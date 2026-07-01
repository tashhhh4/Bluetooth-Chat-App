import logging
import threading
import time
from android.broadcast import BroadcastReceiver
from jnius import autoclass, cast

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
ParcelUuid = autoclass('android.os.ParcelUuid')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
UUID = autoclass('java.util.UUID')

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
        logging.info('Running service listener socket for', ttl, 'seconds.')
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()


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
