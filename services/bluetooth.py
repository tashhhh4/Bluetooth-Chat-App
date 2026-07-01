from android.broadcast import BroadcastReceiver
from jnius import autoclass

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

def handle_intent(context, intent):
    print('Running handle_intent')
    print('context is:', context)
    print('intent is:', intent)
    print('action is:', intent.getAction())

device_receiver = BroadcastReceiver(
    callback=handle_intent,
    actions=[
        BluetoothDevice.ACTION_FOUND,
        BluetoothAdapter.ACTION_DISCOVERY_FINISHED,
    ]
)

def turn_discoverability_on():
    activity = PythonActivity.mActivity
    intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
    intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)

    activity.startActivity(intent)

def turn_discovery_on():
    device_receiver.start()
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_adapter.startDiscovery()

def turn_discovery_off():
    device_receiver.stop()
    bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
    bluetooth_adapter.cancelDiscovery()