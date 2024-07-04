package org.tensorflow.lite.examples.objectdetection

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Context
import android.util.Log
import java.io.IOException
import java.util.UUID

class BluetoothHelper(private val context: Context) {
    private val bluetoothAdapter: BluetoothAdapter? = BluetoothAdapter.getDefaultAdapter()
    private var bluetoothSocket: BluetoothSocket? = null
    private val uuid: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB") // Standard SerialPortService ID

    fun isBluetoothSupported(): Boolean {
        return bluetoothAdapter != null
    }

    fun isBluetoothEnabled(): Boolean {
        return bluetoothAdapter?.isEnabled == true
    }

    fun connectToDevice(address: String): Boolean {
        val device: BluetoothDevice? = bluetoothAdapter?.getRemoteDevice(address)
        try {
            bluetoothSocket = device?.createRfcommSocketToServiceRecord(uuid)
            bluetoothSocket?.connect()
            bluetoothSocket?.outputStream?.write("connected\n".toByteArray())
            return true
        } catch (e: IOException) {
            Log.e("BluetoothHelper", "Could not connect to device: ${e.message}")
            return false
        }
    }

    fun sendData(data: String) {
        try {
            // Ajouter un caractère de nouvelle ligne à la fin des données
            val dataWithNewline = "$data\n"
            bluetoothSocket?.outputStream?.write(dataWithNewline.toByteArray())
            bluetoothSocket?.outputStream?.flush()  // Forcer l'envoi immédiat des données
        } catch (e: IOException) {
            Log.e("BluetoothHelper", "Error sending data: ${e.message}")
        }
    }

    fun closeConnection() {
        try {
            bluetoothSocket?.close()
        } catch (e: IOException) {
            Log.e("BluetoothHelper", "Error closing Bluetooth connection: ${e.message}")
        }
    }

    fun startDiscovery() {
        bluetoothAdapter?.startDiscovery()
    }

    fun cancelDiscovery() {
        bluetoothAdapter?.cancelDiscovery()
    }
}