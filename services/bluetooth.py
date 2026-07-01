from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
print('BluetoothAdapter is a', type(BluetoothAdapter))

def turn_discoverability_on():
    activity = PythonActivity.mActivity
    intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
    intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)

    activity.startActivity(intent)

def turn_discovery_on():
    print('Running turn_discovery_on')
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_adapter.startDiscovery()

def turn_discovery_off():
    print('Running turn_discovery_off')
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_adapter.cancelDiscovery()