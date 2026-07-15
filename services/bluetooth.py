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
from services.android import AndroidService
from services.connection import Connection

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
Intent = autoclass('android.content.Intent')
ParcelUuid = autoclass('android.os.ParcelUuid')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
JavaUUID = autoclass('java.util.UUID')

class BluetoothService :

    def __init__(self):

        self.is_scanning = False
        self.discovered_devices = {}
        self.connection = Connection(None)

        self.event_registry = EventRegistry(
            [
                'BONDED_DEVICES_UPDATED',
                'CONNECTION_ESTABLISHED',
                'CONNECTION_LOST',
                'DISCOVERED_DEVICES_UPDATED',
                'MESSAGE_RECEIVED',
            ], 'BluetoothService.event_registry'
        )

        self.device_receiver = self._get_device_receiver()
        self.android_service = self._get_android_service()

    @staticmethod
    def turn_discoverability_on(ttl): # max 300
        activity = PythonActivity.mActivity
        intent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        intent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, ttl)

        activity.startActivity(intent)

    def load_paired_devices(self):
        def l():
            bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
            devices_set = bluetooth_adapter.getBondedDevices()
            devices_list = [{'name': dev.name, 'address': dev.address} for dev in devices_set]
            self.event_registry.emit_event('BONDED_DEVICES_UPDATED', devices_list)
        def d():
            logging.info('BluetoothService: User blocked access to BLUETOOTH_CONNECT.')
        self.android_service.run_with_permissions(['android.permission.BLUETOOTH_CONNECT'], l, d)

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
        self.android_service.run_with_permissions(['android.permission.BLUETOOTH_CONNECT'], l, d)

    def connect_to_device(self, address):
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        device = bluetooth_adapter.getRemoteDevice(address)
        if not device:
            logging.info('Device not found!')
            return

        java_uuid = JavaUUID.fromString(str(SERVICE_UUID))

        connector_socket = device.createRfcommSocketToServiceRecord(java_uuid)

        connect_on_thread(
            connector_socket,
            name='Connection Initiator',
            on_connected=self._handle_connection,
        )

    def start_reading_input_stream(self):
        if self.connection.socket is None:
            raise IOError('No connection.')
        input_stream = self.connection.socket.getInputStream()
        thread = read_input_stream_on_thread(
            self.connection.socket,
            input_stream,
            name='Input Stream Reader',
            on_receive=self._handle_receive,
            on_disconnect=self._handle_connection_lost,
        )

    def send_bytes(self, data):
        self.connection.send_bytes(data)

    def scan_for_devices(self):
        logging.info('Scanning for devices...')
        self.is_scanning = True
        self._turn_discovery_on()

    def stop_scanning(self):
        self._turn_discovery_off()
        self.is_scanning = False
        logging.info('Scanning stopped.')

    def _turn_discovery_on(self):
        self.device_receiver = self._get_device_receiver()
        self.device_receiver.start()
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.startDiscovery()
        logging.info('Discovery started.')

    def _turn_discovery_off(self):
        if self.device_receiver:
            self.device_receiver.stop()
            self.device_receiver = None
        bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()
        bluetooth_adapter.cancelDiscovery()
        logging.info('Discovery cancelled.')

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

    def _get_android_service(self):
        android_service = AndroidService()
        android_service.event_registry.register_event_callback('PERMISSION_GRANTED', self._handle_permission_granted)
        return android_service

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

    def _handle_permission_granted(self, permission):
        if permission == 'android.permission.BLUETOOTH_CONNECT':
            self._handle_bluetooth_connect_permission_granted()

    def _handle_bluetooth_connect_permission_granted(self):
        self.load_paired_devices()

    def _handle_connection(self, socket):
        logging.debug('[BluetoothService] Running _handle_connection()')
        self.connection.socket = socket
        logging.debug('[BluetoothService] emits CONNECTION_ESTABLISHED')
        self.event_registry.emit_event('CONNECTION_ESTABLISHED')

        self.start_reading_input_stream()

    def _handle_connection_lost(self):
        logging.debug('BluetoothService: emits CONNECTION_LOST.')
        self.event_registry.emit_event('CONNECTION_LOST')

    def _handle_receive(self, data):
        logging.debug('[BluetoothService] Running_handle_receive(data)')
        logging.debug(f'BluetoothService: Received {data}')
        logging.debug('[BluetoothService] emits MESSAGE_RECEIVED')
        self.event_registry.emit_event('MESSAGE_RECEIVED', data)