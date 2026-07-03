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

class BluetoothService:

    device_receiver = None

    is_scanning = False

    discovered_devices = {}
    _callbacks = {
        'DISCOVERED_DEVICES_UPDATED': [],
    }

    def __init__(self):
        self.device_receiver = self._get_device_receiver()

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
    def query_device_for_service_record(device):
        java_uuid = JavaUUID.fromString(str(SERVICE_UUID))
        service_query_socket = device.createRfcommSocketToServiceRecord(java_uuid)
        print('Created socket:', service_query_socket)
        try:
            result = service_query_socket.connect()
            print('After attempting to use connect()')
            print('Socket is:', service_query_socket)
            print('Result is:', result)
            return result
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def turn_discoverability_on(ttl): # max 300
        activity = PythonActivity.mActivity
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, ttl)

        activity.startActivity(intent)

    def scan_for_devices(self):
        print('Scanning for devices...')
        self.is_scanning = True
        self._turn_discovery_on()

    def stop_scanning(self):
        self._turn_discovery_off()
        self.is_scanning = False
        print('Scanning stopped.')

    def register_event_callback(self, event_name, callback):
        if event_name not in self._callbacks:
            raise TypeError(f'No event called {event_name} for service BluetoothService')
        self._callbacks[event_name].append(callback)

    def _emit_event(self, event_name, *args, **kwargs):
        for callback in self._callbacks[event_name]:
            callback(*args, **kwargs)

    def _turn_discovery_on(self):
        self.device_receiver = self._get_device_receiver()
        self.device_receiver.start()
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.startDiscovery()
        print('Discovery started.')

    def _turn_discovery_off(self):
        if self.device_receiver:
            self.device_receiver.stop()
            self.device_receiver = None
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
        print('Discovery cancelled.')

    def _add_discovered_device(self, device):
        # check if a device with this address is already in our discovered_devices
        if device.address not in self.discovered_devices:
            self.discovered_devices[device.address] = {
                'name': device.name,
            }
            print(f'Discovered device ({device.name}): {device.address})')
        list_ = [{'name': n['name'], 'address': a} for a, n in self.discovered_devices.items()]
        self._emit_event('DISCOVERED_DEVICES_UPDATED', list_)

    def _get_device_receiver(self):
        device_receiver = BroadcastReceiver(
            callback=self._handle_intent,
            actions=[
                BluetoothDevice.ACTION_FOUND,
            ],
        )
        return device_receiver

    def _handle_device_found(self, intent):
        # self._turn_discovery_off()
        print('Running _handle_device_found.')

        parcelable = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
        device = cast(BluetoothDevice, parcelable)

        self._add_discovered_device(device)
        # result = self.query_device_for_service_record(device)
        # if self.is_scanning:
        #     self._turn_discovery_on()

    def _handle_intent(self, _, intent):
        action = intent.getAction()

        if action == BluetoothDevice.ACTION_FOUND:
            self._handle_device_found(intent)
