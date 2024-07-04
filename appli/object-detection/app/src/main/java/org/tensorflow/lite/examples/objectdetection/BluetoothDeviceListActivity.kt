package org.tensorflow.lite.examples.objectdetection

import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class BluetoothDeviceListActivity : AppCompatActivity() {

    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var pairedDevicesListView: ListView
    private lateinit var availableDevicesListView: ListView
    private lateinit var pairedDevicesAdapter: ArrayAdapter<String>
    private lateinit var availableDevicesAdapter: ArrayAdapter<String>

    private val deviceClickListener = AdapterView.OnItemClickListener { parent, _, position, _ ->
        bluetoothAdapter.cancelDiscovery()

        val info = (parent.getItemAtPosition(position) as String).split("\n").toTypedArray()
        val address = info[1]
        val intent = Intent()
        intent.putExtra("deviceAddress", address)
        setResult(Activity.RESULT_OK, intent)
        finish()
    }

    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            when(intent.action) {
                BluetoothDevice.ACTION_FOUND -> {
                    val device: BluetoothDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)!!
                    val deviceName = device.name ?: "Unknown Device"
                    val deviceHardwareAddress = device.address
                    val deviceInfo = "$deviceName\n$deviceHardwareAddress"
                    availableDevicesAdapter.add(deviceInfo)
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_bluetooth_device_list)

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

        pairedDevicesListView = findViewById(R.id.paired_devices_list)
        availableDevicesListView = findViewById(R.id.available_devices_list)

        pairedDevicesAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1)
        availableDevicesAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1)

        pairedDevicesListView.adapter = pairedDevicesAdapter
        availableDevicesListView.adapter = availableDevicesAdapter

        pairedDevicesListView.onItemClickListener = deviceClickListener
        availableDevicesListView.onItemClickListener = deviceClickListener

        val pairedDevices: Set<BluetoothDevice>? = bluetoothAdapter?.bondedDevices
        pairedDevices?.forEach { device ->
            val deviceName = device.name
            val deviceHardwareAddress = device.address
            pairedDevicesAdapter.add("$deviceName\n$deviceHardwareAddress")
        }

        val filter = IntentFilter(BluetoothDevice.ACTION_FOUND)
        registerReceiver(receiver, filter)

        bluetoothAdapter?.startDiscovery()
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(receiver)
    }
}