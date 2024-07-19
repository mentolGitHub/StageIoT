import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:sensors_plus/sensors_plus.dart';
import 'package:geolocator/geolocator.dart';
import 'package:light/light.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'dart:typed_data';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sensor Data App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MainPage(),
    );
  }
}

class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  BluetoothDevice? _selectedDevice;
  BluetoothConnection? _connection;
  bool _isConnected = false;
  bool _use4G5G = false;
  bool _detectObjects = false;
  String _serverIP = '';
  Timer? _sensorTimer;
  bool _isSendingData = false;
  String _eui = '1111111111111111';

  // Sensor data
  Position? _position;
  double _luminosity = 0;
  GyroscopeEvent? _gyroscope;
  double _pressure = 0;
  AccelerometerEvent? _accelerometer;
  double _angle = 0;
  double _azimuth = 0;

  // External sensor data
  double _distance = 0;
  double _externalHumidity = 0;
  double _externalTemperature = 0;
  String _objectDetectionData = '';

  // Sensor streams
  StreamSubscription<Position>? _positionSubscription;
  StreamSubscription<int>? _luminositySubscription;
  StreamSubscription<GyroscopeEvent>? _gyroscopeSubscription;
  StreamSubscription<AccelerometerEvent>? _accelerometerSubscription;

  @override
  void initState() {
    super.initState();
    _initSensors();
  }

  @override
  void dispose() {
    _stopSensorReading();
    _connection?.dispose();
    super.dispose();
  }

  void _initSensors() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled.');
    }
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permissions are denied');
      }
    }
    _positionSubscription =
        Geolocator.getPositionStream().listen((Position position) {
      setState(() {
        _position = position;
      });
    });

    Light().lightSensorStream.listen((int luxValue) {
      setState(() {
        _luminosity = luxValue.toDouble();
      });
    });

    _gyroscopeSubscription = gyroscopeEvents.listen((GyroscopeEvent event) {
      setState(() {
        _gyroscope = event;
      });
    });

    _accelerometerSubscription =
        accelerometerEvents.listen((AccelerometerEvent event) {
      setState(() {
        _accelerometer = event;
      });
    });

    // Note: Angle, Azimuth, and Pressure typically require more complex calculations
    // You might need to use additional sensors or libraries to get these values accurately
  }

  void _stopSensorReading() {
    _positionSubscription?.cancel();
    _luminositySubscription?.cancel();
    _gyroscopeSubscription?.cancel();
    _accelerometerSubscription?.cancel();
  }

  void _selectBT() async {
    final BluetoothDevice? selectedDevice =
        await Navigator.of(context).push(MaterialPageRoute(
      builder: (context) {
        return SelectBondedDevicePage(checkAvailability: false);
      },
    ));

    if (selectedDevice != null) {
      setState(() {
        _selectedDevice = selectedDevice;
      });
      _connectToBluetooth();
    }
  }

  void _connectToBluetooth() async {
    if (_selectedDevice == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No device selected')),
      );
      return;
    }

    try {
      _connection =
          await BluetoothConnection.toAddress(_selectedDevice!.address);
      setState(() {
        _isConnected = true;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Connected to ${_selectedDevice!.name}')),
      );

      _connection!.input!.listen(_processIncomingBluetoothData).onDone(() {
        setState(() {
          _isConnected = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Disconnected from ${_selectedDevice!.name}')),
        );
      });
    } catch (e) {
      setState(() {
        _isConnected = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error connecting to device: $e')),
      );
    }
  }

  void _toggleSendData() {
    setState(() {
      _isSendingData = !_isSendingData;
    });

    if (_isSendingData) {
      _startSendingData();
    } else {
      _stopSendingData();
    }
  }

  void _startSendingData() {
    _sensorTimer = Timer.periodic(Duration(milliseconds: 100), (timer) {
      if (_use4G5G) {
        _sendDataToServer();
      } else if (_isConnected) {
        _sendDataViaBluetooth();
      } else {
        _stopSendingData();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content:
                  Text('Please connect to a Bluetooth device or enable 4G/5G')),
        );
      }
    });
  }

  void _stopSendingData() {
    _sensorTimer?.cancel();
    _sensorTimer = null;
  }

  String _formatData() {
    if (_position == null || _gyroscope == null || _accelerometer == null) {
      return '';
    }

    return '2$_eui,${DateTime.now().millisecondsSinceEpoch},' +
        '${_position!.latitude},${_position!.longitude},${_position!.altitude},' +
        '$_luminosity,' +
        '${_gyroscope!.x},${_gyroscope!.y},${_gyroscope!.z},' +
        '$_pressure,' +
        '${_accelerometer!.x},${_accelerometer!.y},${_accelerometer!.z},' +
        '$_angle,$_azimuth,' +
        '$_distance,$_externalHumidity,$_externalTemperature';
  }

  Future<void> _sendDataToServer() async {
    if (_serverIP.isEmpty) {
      _stopSendingData();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a server IP')),
      );
      return;
    }

    String formattedData = _formatData();
    if (formattedData.isEmpty) {
      return; // Not all sensor data is available yet
    }

    try {
      final response = await http.post(
        Uri.parse('http://$_serverIP/post_data'),
        headers: {'Content-Type': 'text/plain'},
        body: formattedData,
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to send data');
      }

      // Send object detection data if available
      if (_objectDetectionData.isNotEmpty) {
        final objectResponse = await http.post(
          Uri.parse('http://$_serverIP/post_data'),
          headers: {'Content-Type': 'text/plain'},
          body: '4 $_objectDetectionData',
        );

        if (objectResponse.statusCode != 200) {
          throw Exception('Failed to send object detection data');
        }
      }
    } catch (e) {
      _stopSendingData();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending data: $e')),
      );
    }
  }

  Future<void> _sendDataViaBluetooth() async {
    if (_connection == null || !_connection!.isConnected) {
      _stopSendingData();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Not connected to a Bluetooth device')),
      );
      return;
    }

    String formattedData = _formatData();
    if (formattedData.isEmpty) {
      return; // Not all sensor data is available yet
    }

    try {
      Uint8List bytes = Uint8List.fromList(utf8.encode(formattedData));
      _connection!.output.add(bytes);
      await _connection!.output.allSent;
    } catch (e) {
      _stopSendingData();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending data via Bluetooth: $e')),
      );
    }
  }

  void _processIncomingBluetoothData(Uint8List data) {
    String message = utf8.decode(data);
    if (message.startsWith('0')) {
      if (message[1] == '1') {
        _eui = message.substring(2);
      }
    }
    if (message.startsWith('3')) {
      // External sensor data
      List<String> parts = message.substring(2).split(',');
      if (parts.length == 3) {
        setState(() {
          _distance = double.parse(parts[0]);
          _externalHumidity = double.parse(parts[1]);
          _externalTemperature = double.parse(parts[2]);
        });
      }
    } else if (message.startsWith('4')) {
      // Object detection data
      setState(() {
        _objectDetectionData = message.substring(2); // Store the raw data
      });
    }
  }

  void _validateParameters() {
    if (_use4G5G && _serverIP.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a server IP for 4G/5G mode')),
      );
      return;
    }

    if (!_use4G5G && !_isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content: Text(
                'Please connect to a Bluetooth device for Bluetooth mode')),
      );
      return;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Sensor Data App')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: _selectBT,
              child: Text('Select Bluetooth Device'),
            ),
            SizedBox(height: 10),
            Text(_isConnected ? 'Connected' : 'Disconnected'),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _toggleSendData,
              child:
                  Text(_isSendingData ? 'Stop Sending' : 'Start Sending Data'),
            ),
            SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Use 4G/5G'),
                Switch(
                  value: _use4G5G,
                  onChanged: (value) {
                    setState(() {
                      _use4G5G = value;
                    });
                  },
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Detect Objects'),
                Switch(
                  value: _detectObjects,
                  onChanged: (value) {
                    setState(() {
                      _detectObjects = value;
                    });
                  },
                ),
              ],
            ),
            SizedBox(height: 10),
            TextField(
              decoration: InputDecoration(labelText: 'Server IP'),
              onChanged: (value) {
                setState(() {
                  _serverIP = value;
                });
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _validateParameters,
              child: Text('Validate Parameters'),
            ),
            SizedBox(height: 20),
            Text('External Sensors:'),
            Text('Distance: $_distance'),
            Text('Humidity: $_externalHumidity'),
            Text('Temperature: $_externalTemperature'),
            SizedBox(height: 20),
            Text('Received Object Detection Data:'),
            Text(_objectDetectionData.isNotEmpty
                ? _objectDetectionData
                : 'No object detection data received'),
          ],
        ),
      ),
    );
  }
}

class SelectBondedDevicePage extends StatelessWidget {
  final bool checkAvailability;

  const SelectBondedDevicePage({Key? key, this.checkAvailability = true})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Select Bluetooth Device'),
      ),
      body: FutureBuilder(
        future: FlutterBluetoothSerial.instance.getBondedDevices(),
        builder: (context, AsyncSnapshot<List<BluetoothDevice>> snapshot) {
          if (snapshot.hasData) {
            return ListView(
              children: snapshot.data!.map((device) {
                return ListTile(
                  title: Text(device.name ?? "Unknown device"),
                  subtitle: Text(device.address),
                  onTap: () {
                    Navigator.of(context).pop(device);
                  },
                );
              }).toList(),
            );
          } else {
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
