package com.example.iotapp;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okhttp3.Response;
import okio.ByteString;
import android.annotation.SuppressLint;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.OnSuccessListener;

import org.json.JSONObject;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationResult;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.ZoneOffset;

public class MainActivity extends AppCompatActivity {

    Button btnConnectWifi;
    TextView tSocket;
    TextView sData;

    private boolean hasStartedAfterWifi = false;


    private boolean isSocketConnected = false;

    private final String SERVER_IP = "10.42.0.1";
    private final int SERVER_PORT = 6789;

    private WebSocket webSocket;
    private OkHttpClient client;

    private FusedLocationProviderClient fusedLocationClient;
    private LocationCallback locationCallback;

    private SensorManager sensorManager;
    private float[] gravity = new float[3];
    private float[] geomagnetic = new float[3];
    private float lastPitch = 0f;
    private float lastRoll = 0f;
    private float lastOrientation=0f;

    /*
        * Listener to collect the pitch and roll data of the phone,, useful for the pitch and roll of the vehicule
    */
    private final SensorEventListener sensorListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
                gravity = event.values.clone();
            } else if (event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
                geomagnetic = event.values.clone();
            }

            float R[] = new float[9];
            float I[] = new float[9];

            if (SensorManager.getRotationMatrix(R, I, gravity, geomagnetic)) {
                float[] orientation = new float[3];
                SensorManager.getOrientation(R, orientation);
                lastOrientation= (float) Math.toDegrees(orientation[0]);
                lastPitch = (float) Math.toDegrees(orientation[1]); // avant/arrière
                lastRoll = (float) Math.toDegrees(orientation[2]);  // gauche/droite
            }
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);

        setContentView(R.layout.activity_main);


        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        Sensor accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        Sensor magnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);



        sensorManager.registerListener(sensorListener, accelerometer, SensorManager.SENSOR_DELAY_UI);
        sensorManager.registerListener(sensorListener, magnetometer, SensorManager.SENSOR_DELAY_UI);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        btnConnectWifi = findViewById(R.id.wifi);
        tSocket= findViewById(R.id.socketConnected);
        tSocket.setText(R.string.no_co_sock);
        sData= findViewById(R.id.sendData);

        //la localisation

        checkWifiConnection();

    }


    /*
        *Check if yhe phone is connected to the access point
     */
    private void checkWifiConnection() {
        ConnectivityManager connManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo wifiInfo = connManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI);

        boolean isConnected = wifiInfo != null && wifiInfo.isConnected();

        if (isConnected) {
            btnConnectWifi.setEnabled(false);
            Toast.makeText(this, "Connecté au Wi-Fi", Toast.LENGTH_SHORT).show();
            if(!hasStartedAfterWifi){
                connectWebSocket();   // Connexion au démarrage
                startLocationUpdates();
                hasStartedAfterWifi=true;
            }




        } else {
            hasStartedAfterWifi=false;
            btnConnectWifi.setEnabled(true);
            sData.setText("");
            tSocket.setText(R.string.no_co_sock);
            Toast.makeText(this, "Non connecté au Wi-Fi", Toast.LENGTH_SHORT).show();

            btnConnectWifi.setOnClickListener(v -> {
                Intent intent = new Intent(Settings.ACTION_WIFI_SETTINGS);
                startActivity(intent);
            });
        }
    }


    /*
        * Connect to the plateform using websocket API, useful for sending all the collected data
    */
    private void connectWebSocket() {
        client = new OkHttpClient();

        Request request = new Request.Builder()
                .url("ws://" + SERVER_IP + ":" + SERVER_PORT) // Modifie le chemin si besoin
                .build();

        webSocket = client.newWebSocket(request, new WebSocketListener() {
            @Override
            public void onOpen(@NonNull WebSocket webSocket, @NonNull Response response) {
                Log.d("WEBSOCKET", "Connecté !");
                isSocketConnected = true;
                tSocket.setText(R.string.co_sock);
            }

            @Override
            public void onMessage(@NonNull WebSocket webSocket, @NonNull String text) {
                Log.d("WEBSOCKET", "Message reçu : " + text);
            }

            @Override
            public void onFailure(@NonNull WebSocket webSocket, @NonNull Throwable t, Response response) {
                Log.e("WEBSOCKET", "Erreur : " + t.getMessage());
                isSocketConnected = false;
                tSocket.setText(R.string.no_co_sock);
                sData.setText("");
            }

            @Override
            public void onClosing(@NonNull WebSocket webSocket, int code, @NonNull String reason) {
                webSocket.close(1000, null);
                Log.d("WEBSOCKET", "Fermeture : " + reason);
            }
        });
    }


    /*
        * Sending the data collected each second
    */
    private void sendPosition(double lat, double lon, float speed,double alt) {
        if (isSocketConnected && webSocket != null) {
            try {

                ZonedDateTime nowUtc = null;
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    nowUtc = ZonedDateTime.now(ZoneOffset.UTC);
                }
                String isoTimestamp = null;
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    isoTimestamp = nowUtc.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
                }

                JSONObject json = new JSONObject();
                json.put("timestamp", isoTimestamp);
                json.put("latitude", lat);
                json.put("longitude", lon);
                json.put("altitude",alt);
                json.put("speed", speed);
                json.put("pitch", lastPitch);
                json.put("roll", lastRoll);
                json.put("azimuth", lastOrientation);


                String message = json.toString();
                webSocket.send(message);
                sData.setText(R.string.sendD);
                Log.d("WEBSOCKET", "JSON envoyé : " + message);
            } catch (Exception e) {
                Log.e("WEBSOCKET", "Erreur JSON : " + e.getMessage());
            }
        }
    }

    /*
        * Update the location of the user, each second
     */
    private void startLocationUpdates() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            return;
        }

        LocationRequest locationRequest = new LocationRequest.Builder(
                LocationRequest.PRIORITY_HIGH_ACCURACY,
                1000L // Demande toutes les 1s
        ).setMinUpdateIntervalMillis(500L)
                .build();

        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(@NonNull LocationResult locationResult) {
                if (locationResult == null) return;

                for (Location location : locationResult.getLocations()) {
                    double lat = location.getLatitude();
                    double lon = location.getLongitude();
                    float speed = location.getSpeed(); // m/s
                    double altitude = location.getAltitude();
                    sendPosition(lat, lon, speed, altitude); // 🔁 Envoie dès réception
                }
            }
        };

        fusedLocationClient.requestLocationUpdates(locationRequest, locationCallback, Looper.getMainLooper());
    }

    /*
        * Free all the allocated ressources
     */
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (locationCallback != null) {
            fusedLocationClient.removeLocationUpdates(locationCallback);
        }
    }

    /*
        * Check if the phone is still connected to the access point
    */
    @Override
    protected void onResume() {
        super.onResume();

        checkWifiConnection();

        if(!isSocketConnected){
            connectWebSocket();
        }
    }
}