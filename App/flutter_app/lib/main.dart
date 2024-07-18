import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:sensors_plus/sensors_plus.dart';
import 'package:webview_flutter/webview_flutter.dart';

class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  bool _isConnected = false;
  bool _use4G5G = false;
  bool _detectObjects = false;
  String _serverIP = '';

  void _selectBT() {
    // Implement Bluetooth device selection
  }

  void _sendData() {
    // Implement data sending logic
  }

  void _exportData() {
    // Implement data export functionality
  }

  void _validateParameters() {
    // Implement parameter validation
    // If valid, navigate to WebView
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => GoogleWebView()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('My App')),
      body: Column(
        children: [
          ElevatedButton(onPressed: _selectBT, child: Text('selectionner BT')),
          ElevatedButton(onPressed: _sendData, child: Text('Send_data')),
          // Add other UI elements here
          ElevatedButton(
            onPressed: _validateParameters,
            child: Text('valider les parametres'),
          ),
        ],
      ),
    );
  }
}

class GoogleWebView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Google')),
      body: WebView(
        initialUrl: 'https://www.google.com',
        javascriptMode: JavascriptMode.unrestricted,
      ),
    );
  }
}
