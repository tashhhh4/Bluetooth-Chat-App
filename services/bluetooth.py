import logging
from android.broadcast import BroadcastReceiver
from jnius import autoclass, cast
from config import SERVICE_UUID
from utils import (
    accept_on_thread,
    connect_on_thread,
    read_input_stream_on_thread,
    EventRegistry
)
from services.platform import run_with_permissions

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
ParcelUuid = autoclass('android.os.ParcelUuid')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
JavaUUID = autoclass('java.util.UUID')

class BluetoothService :

    device_receiver = None
    connected_socket = None

    is_scanning = False

    discovered_devices = {}

    event_registry = EventRegistry([
        'BONDED_DEVICES_UPDATED',
        'CONNECTION_ESTABLISHED',
        'DISCOVERED_DEVICES_UPDATED',
        'MESSAGE_RECEIVED',
        ], 'BluetoothService.event_registry'
    )

    def __init__(self):
        self.device_receiver = self._get_device_receiver()

    @staticmethod
    def turn_discoverability_on(ttl): # max 300
        activity = PythonActivity.mActivity
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, ttl)

        activity.startActivity(intent)

    def load_paired_devices(self):
        print('Running BluetoothService load_paired_devices()')
        def l():
            print('Running callback l() in load_paired_devices')
            bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
            devices_set = bluetooth_adapter.getBondedDevices()
            print('Retrieved bonded devices. Set is:', devices_set)
            devices_list = [{'name': dev.name, 'address': dev.address} for dev in devices_set]
            print('Turned devices into formatted list of dicts:', devices_list)
            self.event_registry.emit_event('BONDED_DEVICES_UPDATED', devices_list)
        def d():
            logging.info('BluetoothService: User blocked access to BLUETOOTH_CONNECT.')
        run_with_permissions(['android.permission.BLUETOOTH_CONNECT'], l, d)

    def listen_for_connections(self):
        def l():
            bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
            java_uuid = JavaUUID.fromString(str(SERVICE_UUID))

            connection_listener_socket = bluetooth_adapter.listenUsingRfcommWithServiceRecord('Blu', java_uuid)

            accept_on_thread(
                connection_listener_socket,
                name='Connection Listener',
                on_connected=self._handle_connection,
            )
        def d():
            logging.info('BluetoothService: User blocked access to BLUETOOTH_CONNECT.')
        run_with_permissions(['android.permission.BLUETOOTH_CONNECT'], l, d)

    def connect_to_device(self, address):
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        device = bluetooth_adapter.getRemoteDevice(address)
        if not device:
            print('Device not found!')
            return

        java_uuid = JavaUUID.fromString(str(SERVICE_UUID))

        connector_socket = device.createRfcommSocketToServiceRecord(java_uuid)

        connect_on_thread(
            connector_socket,
            name='Connection Initiator',
            on_connected=self._handle_connection,
        )

    def start_reading_input_stream(self):
        if self.connected_socket is None:
            raise IOError('No connection.')
        input_stream = self.connected_socket.getInputStream()
        thread = read_input_stream_on_thread(
            self.connected_socket,
            input_stream,
            name='Input Stream Reader',
            on_receive=self._handle_receive,
        )

    def send_bytes(self, data):
        if self.connected_socket is None:
            raise IOError('No connection.')
        output_stream = self.connected_socket.getOutputStream()
        try:
            output_stream.write(data.encode('utf-8'))
            output_stream.flush()
        except Exception as e:
            print('send_bytes error:', e)

    def scan_for_devices(self):
        print('Scanning for devices...')
        self.is_scanning = True
        self._turn_discovery_on()

    def stop_scanning(self):
        self._turn_discovery_off()
        self.is_scanning = False
        print('Scanning stopped.')

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
        list_ = [{'name': n['name'], 'address': a} for a, n in self.discovered_devices.items()]
        self.event_registry.emit_event('DISCOVERED_DEVICES_UPDATED', list_)

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

    def _handle_connection(self, socket):
        logging.info('[BluetoothService] Running _handle_connection()')
        self.connected_socket = socket
        logging.info('[BluetoothService] emits CONNECTION_ESTABLISHED')
        self.event_registry.emit_event('CONNECTION_ESTABLISHED')


        self.start_reading_input_stream()

    def _handle_receive(self, data):
        logging.info('[BluetoothService] Running_handle_receive(data)')
        logging.info(f'BluetoothService: Received {data}')
        logging.info('[BluetoothService] emits MESSAGE_RECEIVED')
        self.event_registry.emit_event('MESSAGE_RECEIVED', data)