import socket
import subprocess
import logging
from PySide6.QtBluetooth import (
    QBluetoothAddress,
    QBluetoothLocalDevice,
    QBluetoothSocket,
    QBluetoothServer,
    QBluetoothServiceInfo,
    QBluetoothUuid,
)
from PySide6.QtCore import QUuid
from services.bluetooth import BluetoothService
from config import SERVICE_UUID
#from utils import accept_on_thread_qt

def run_command(*args):
    return subprocess.run([*args], capture_output=True, text=True, check=True).stdout

class DesktopBluetoothService(BluetoothService):

    def __init__(self):

        super().__init__(events=[
            'BONDED_DEVICES_UPDATED',
            'CONNECTION_ESTABLISHED',
            'DISCOVERED_DEVICES_UPDATED',
        ])

        self.connection_listener_server = None
        self.spp_service = None

    @staticmethod
    def whats_my_mac_address():
        # run bluetoothctl to find out
        stdout = run_command('bluetoothctl', 'show')
        address = None
        for line in stdout.splitlines():
            if 'Controller' in line:
                parts = line.split(' ')
                address = parts[1]
                break
        return address

    def load_paired_devices(self):

        # run bluetoothctl devices
        command_result = subprocess.run(
            ['bluetoothctl', 'devices'],
            capture_output=True,
            text=True,
            check=True, # Raise an exception if something goes wrong with the command.
        )

        # convert the string output into a list of data about the devices (name and address)
        lines = command_result.stdout.splitlines()
        devices = []
        for line in lines:
            parts = line.split(' ')
            address = parts[1]
            name = ' '.join(parts[2:])
            devices.append({'name': name, 'address': address})

        self.event_registry.emit_event('BONDED_DEVICES_UPDATED', devices)

    def listen_for_connections(self):
        logging.warning('Listen for connections - not yet implemented in DesktopBluetoothService')

        address = QBluetoothLocalDevice().address()

        # Create server
        self.connection_listener_server = QBluetoothServer(QBluetoothServiceInfo.RfcommProtocol)
        self.connection_listener_server.listen(address)
        logging.info('Server is listening...')

        # Create service
        self.spp_service = QBluetoothServiceInfo()
        self.spp_service.setServiceName('Blu2')
        self.spp_service.setServiceDescription('Bluetooth Chat')
        self.spp_service.setServiceProvider('Blu2')
        self.spp_service.setServiceUuid(QBluetoothUuid(QUuid(str(SERVICE_UUID))))

        # Describe the protocol
        rfcomm = QBluetoothServiceInfo.Sequence()
        rfcomm.append(QBluetoothUuid(QBluetoothUuid.ProtocolUuid.Rfcomm))
        rfcomm.append(self.connection_listener_server.serverPort())

        l2cap = QBluetoothServiceInfo.Sequence()
        l2cap.append(QBluetoothUuid(QBluetoothUuid.ProtocolUuid.L2cap))

        protocols = QBluetoothServiceInfo.Sequence()
        protocols.append(l2cap)
        protocols.append(rfcomm)

        self.spp_service.setAttribute(
            QBluetoothServiceInfo.AttributeId.ProtocolDescriptorList.value,
            protocols
        )

        # Register the service
        self.spp_service.registerService(address)
        logging.info('Blu2 Service details registered.')

    def connect_to_device(self, address):
        sock = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)
        logging.warning(f'Created socket. The rest of the connect to device function is not yet implemented.')
        address_obj = QBluetoothAddress(address)
        logging.info('Created address_obj:', address_obj)
        # uuid_obj = QBluetoothUuid.ServiceClassUuid(str(SERVICE_UUID))
        # uuid_obj = QBluetoothUuid.ProtocolUuid(str(SERVICE_UUID))
        # uuid_obj = QBluetoothUuid.StringFormat(str(SERVICE_UUID))

        sock.connectToService(address_obj, str(SERVICE_UUID))

    def _handle_connection(self, sock):
        self.event_registry.emit_event('CONNECTION_ESTABLISHED', sock)