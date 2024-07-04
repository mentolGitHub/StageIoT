
import java.lang.System;

@kotlin.Metadata(mv = {1, 6, 0}, k = 1, d1 = {"\u0000:\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0002\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0006\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\u0002\u0010\u0004J\u0006\u0010\u000b\u001a\u00020\fJ\u0006\u0010\r\u001a\u00020\fJ\u000e\u0010\u000e\u001a\u00020\u000f2\u0006\u0010\u0010\u001a\u00020\u0011J\u0006\u0010\u0012\u001a\u00020\u000fJ\u0006\u0010\u0013\u001a\u00020\u000fJ\u000e\u0010\u0014\u001a\u00020\f2\u0006\u0010\u0015\u001a\u00020\u0011J\u0006\u0010\u0016\u001a\u00020\fR\u0010\u0010\u0005\u001a\u0004\u0018\u00010\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0010\u0010\u0007\u001a\u0004\u0018\u00010\bX\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u000e\u0010\t\u001a\u00020\nX\u0082\u0004\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u0017"}, d2 = {"LBluetoothHelper;", "", "context", "Landroid/content/Context;", "(Landroid/content/Context;)V", "bluetoothAdapter", "Landroid/bluetooth/BluetoothAdapter;", "bluetoothSocket", "Landroid/bluetooth/BluetoothSocket;", "uuid", "Ljava/util/UUID;", "cancelDiscovery", "", "closeConnection", "connectToDevice", "", "address", "", "isBluetoothEnabled", "isBluetoothSupported", "sendData", "data", "startDiscovery", "app_debug"})
public final class BluetoothHelper {
    private final android.content.Context context = null;
    private final android.bluetooth.BluetoothAdapter bluetoothAdapter = null;
    private android.bluetooth.BluetoothSocket bluetoothSocket;
    private final java.util.UUID uuid = null;
    
    public BluetoothHelper(@org.jetbrains.annotations.NotNull
    android.content.Context context) {
        super();
    }
    
    public final boolean isBluetoothSupported() {
        return false;
    }
    
    public final boolean isBluetoothEnabled() {
        return false;
    }
    
    public final boolean connectToDevice(@org.jetbrains.annotations.NotNull
    java.lang.String address) {
        return false;
    }
    
    public final void sendData(@org.jetbrains.annotations.NotNull
    java.lang.String data) {
    }
    
    public final void closeConnection() {
    }
    
    public final void startDiscovery() {
    }
    
    public final void cancelDiscovery() {
    }
}