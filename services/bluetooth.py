from android.broadcast import BroadcastReceiver
from jnius import autoclass, cast
from config import SERVICE_UUID
from utils import listen_on_thread

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
ParcelUuid = autoclass('android.os.ParcelUuid')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
JavaUUID = autoclass('java.util.UUID')

def handle_device_found(intent):
    parcelable = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
    device = cast(BluetoothDevice, parcelable)
    device.fetchUuidsWithSdp()

def handle_uuid_fetched(intent):
    raw_uuids = intent.getParcelableArrayExtra(BluetoothDevice.EXTRA_UUID)
    if not raw_uuids:
        print('No UUIDs found.')
        return
    uuids = []
    for u in raw_uuids:
        uuid_obj = cast(ParcelUuid, u)
        uuid_str = str(uuid_obj.toString())
        uuids.append(uuid_str)
    print('Extracted UUIDs are:', uuids)

def handle_intent(_, intent):
    action = intent.getAction()

    if action == BluetoothDevice.ACTION_FOUND:
        handle_device_found(intent)

    # elif action == BluetoothDevice.ACTION_UUID:
    #    handle_uuid_fetched(intent)

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

    @staticmethod
    def listen_for_service_record(ttl):
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
        java_uuid = JavaUUID.fromString(str(SERVICE_UUID))

        service_listener_socket = bluetooth_adapter.listenUsingRfcommWithServiceRecord('Blu2', java_uuid)

        thread = listen_on_thread(
            service_listener_socket,
            ttl=ttl,
            name='Service Listener'
        )
        print('Started thread:', thread)

    @staticmethod
    def turn_discoverability_on(ttl): # max 300
        activity = PythonActivity.mActivity
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, ttl)

        activity.startActivity(intent)

    def turn_discovery_on(self):
        print('Running turn_discovery_on')
        print('receiver is', self.device_receiver)
        self.device_receiver = get_device_receiver()
        self.device_receiver.start()
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.startDiscovery()

    def turn_discovery_off(self):
        print('Running turn_discovery_off')
        print('receiver is', self.device_receiver)
        if self.device_receiver:
            self.device_receiver.stop()
            self.device_receiver = None
        print('receiver is', self.device_receiver)
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
