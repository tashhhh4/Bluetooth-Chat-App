import logging
import threading
import time
from android.broadcast import BroadcastReceiver
from jnius import autoclass, cast
from config import SERVICE_UUID

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
    service_listener_socket = None

    def __init__(self):
        self.device_receiver = get_device_receiver()

    def create_service_listener_socket(self, ttl):
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
        java_uuid = JavaUUID.fromString(str(SERVICE_UUID))
        print('Creating socket...')
        service_listener_socket = bluetooth_adapter.listenUsingRfcommWithServiceRecord('Blu2', java_uuid)
        print('Service Listener socket created.')
        def listen():
            try:
                start_time = time.time()
                while time.time() - start_time < ttl:
                    try:
                        client = service_listener_socket.accept(1000) # 1 second timeout
                        print('Connection accepted!')
                        client.close()
                    except Exception as e:
                        print(e)
                print('Listener loop closed after time limit.')
            finally:
                service_listener_socket.close()
                print('Service Listener socket closed.')

        # start thread
        print('Starting listener thread....')
        thread = threading.Thread(target=listen)
        thread.daemon = True
        thread.start()




    def turn_discoverability_on(self, ttl): # max 300
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
