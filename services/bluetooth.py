from pprint import pprint
from android.broadcast import BroadcastReceiver
from jnius import autoclass, cast

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

def handle_device_found(intent):
    parcelable = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
    device = cast(
        'android.bluetooth.BluetoothDevice',
        parcelable
    )
    device.fetchUuidsWithSdp()

def handle_uuid_fetched(intent):
    print('Running handle_uuid_fetched...')
    # parcelable = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
    # device = cast(
    #     BluetoothDevice,
    #     parcelable
    # )
    # print('Fetched a UUID.')
    # print('device is:', device)

def handle_intent(_, intent):
    action = intent.getAction()

    if action == BluetoothDevice.ACTION_FOUND:
        handle_device_found(intent)

    if action == BluetoothDevice.ACTION_UUID:
        handle_uuid_fetched(intent)

def get_device_receiver():
    device_receiver = BroadcastReceiver(
        callback=handle_intent,
        actions=[
            BluetoothDevice.ACTION_FOUND,
            BluetoothDevice.ACTION_UUID,
        ],
    )
    return device_receiver

class BluetoothService:

    device_receiver = None

    def __init__(self):
        self.device_receiver = get_device_receiver()

    def turn_discoverability_on():
        activity = PythonActivity.mActivity
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)

        activity.startActivity(intent)

    def turn_discovery_on(self):
        self.device_receiver.start()
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.startDiscovery()

    def turn_discovery_off(self):
        self.device_receiver.stop()
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
