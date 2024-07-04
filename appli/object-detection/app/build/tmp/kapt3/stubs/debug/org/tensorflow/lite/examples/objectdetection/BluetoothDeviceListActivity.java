package org.tensorflow.lite.examples.objectdetection;

import java.lang.System;

@kotlin.Metadata(mv = {1, 6, 0}, k = 1, d1 = {"\u0000>\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0012\u0010\u0010\u001a\u00020\u00112\b\u0010\u0012\u001a\u0004\u0018\u00010\u0013H\u0014J\b\u0010\u0014\u001a\u00020\u0011H\u0014R\u0014\u0010\u0003\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082.\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082.\u00a2\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082.\u00a2\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\f\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082.\u00a2\u0006\u0002\n\u0000R\u000e\u0010\r\u001a\u00020\u0007X\u0082.\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u0015"}, d2 = {"Lorg/tensorflow/lite/examples/objectdetection/BluetoothDeviceListActivity;", "Landroidx/appcompat/app/AppCompatActivity;", "()V", "availableDevicesAdapter", "Landroid/widget/ArrayAdapter;", "", "availableDevicesListView", "Landroid/widget/ListView;", "bluetoothAdapter", "Landroid/bluetooth/BluetoothAdapter;", "deviceClickListener", "Landroid/widget/AdapterView$OnItemClickListener;", "pairedDevicesAdapter", "pairedDevicesListView", "receiver", "Landroid/content/BroadcastReceiver;", "onCreate", "", "savedInstanceState", "Landroid/os/Bundle;", "onDestroy", "app_debug"})
public final class BluetoothDeviceListActivity extends androidx.appcompat.app.AppCompatActivity {
    private android.bluetooth.BluetoothAdapter bluetoothAdapter;
    private android.widget.ListView pairedDevicesListView;
    private android.widget.ListView availableDevicesListView;
    private android.widget.ArrayAdapter<java.lang.String> pairedDevicesAdapter;
    private android.widget.ArrayAdapter<java.lang.String> availableDevicesAdapter;
    private final android.widget.AdapterView.OnItemClickListener deviceClickListener = null;
    private final android.content.BroadcastReceiver receiver = null;
    
    public BluetoothDeviceListActivity() {
        super();
    }
    
    @java.lang.Override
    protected void onCreate(@org.jetbrains.annotations.Nullable
    android.os.Bundle savedInstanceState) {
    }
    
    @java.lang.Override
    protected void onDestroy() {
    }
}