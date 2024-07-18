import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:sensors_plus/sensors_plus.dart';
import 'package:webview_flutter/webview_flutter.dart';
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
  Map<String, dynamic> _sensorData = {};

  @override
  void initState() {
    super.initState();
    _startSensorReading();
  }

  @override
  void dispose() {
    _sensorTimer?.cancel();
    _connection?.dispose();
    super.dispose();
  }

  void _startSensorReading() {
    _sensorTimer = Timer.periodic(Duration(milliseconds: 100), (timer) {
      _readSensorData();
    });
  }

  void _readSensorData() {
    accelerometerEvents.listen((AccelerometerEvent event) {
      setState(() {
        _sensorData['accelerometer'] = {
          'x': event.x,
          'y': event.y,
          'z': event.z,
        };
      });
    });

    gyroscopeEvents.listen((GyroscopeEvent event) {
      setState(() {
        _sensorData['gyroscope'] = {
          'x': event.x,
          'y': event.y,
          'z': event.z,
        };
      });
    });

    // Add more sensor readings as needed
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
    } catch (e) {
      setState(() {
        _isConnected = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error connecting to device: $e')),
      );
    }
  }

  void _sendData() async {
    if (_use4G5G) {
      await _sendDataToServer();
    } else if (_isConnected) {
      await _sendDataViaBluetooth();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content:
                Text('Please connect to a Bluetooth device or enable 4G/5G')),
      );
    }
  }

  Future<void> _sendDataToServer() async {
    if (_serverIP.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a server IP')),
      );
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('http://$_serverIP/post_data'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(_sensorData),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Data sent successfully via 4G/5G')),
        );
      } else {
        throw Exception('Failed to send data');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending data: $e')),
      );
    }
  }

  Future<void> _sendDataViaBluetooth() async {
    if (_connection == null || !_connection!.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Not connected to a Bluetooth device')),
      );
      return;
    }

    try {
      String jsonData = json.encode(_sensorData);
      Uint8List bytes = Uint8List.fromList(utf8.encode(jsonData));
      _connection!.output.add(bytes);
      await _connection!.output.allSent;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Data sent successfully via Bluetooth')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending data via Bluetooth: $e')),
      );
    }
  }

  void _exportData() {
    // Implement data export functionality
    print('Exporting data: $_sensorData');
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
              child: Text('selectionner BT'),
            ),
            SizedBox(height: 10),
            Text(_isConnected ? 'Connecté' : 'Déconnecté'),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _sendData,
              child: Text('Send_data'),
            ),
            SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('4g/5g'),
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
                Text('detection d\'objet'),
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
            ElevatedButton(
              onPressed: _exportData,
              child: Text('export data'),
            ),
            SizedBox(height: 10),
            TextField(
              decoration: InputDecoration(labelText: 'IP serveur'),
              onChanged: (value) {
                setState(() {
                  _serverIP = value;
                });
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _validateParameters,
              child: Text('valider les parametres'),
            ),
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
