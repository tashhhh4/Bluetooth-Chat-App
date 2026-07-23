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

        # Create server
        self.connection_listener_server = QBluetoothServer(QBluetoothServiceInfo.RfcommProtocol)

        local_device = QBluetoothLocalDevice()
        print('Got local device:', local_device)

        local_address = local_device.address()
        print('Got local address directly from Qt API:', local_address)

        self.connection_listener_server.listen(local_address)

        print('Started server.listen on local address', local_address)
        print('Server port?', self.connection_listener_server.serverPort())
        print('Server type?', self.connection_listener_server.serverType())

        # Create service
        self.spp_service = QBluetoothServiceInfo()
        print('Created a service:', self.spp_service)

        self.spp_service.setServiceName('Blu2')
        self.spp_service.setServiceDescription('Bluetooth Chat')
        self.spp_service.setServiceProvider('Blu2')

        print('Set the service\'s basic properties.')

        quuid = QUuid(str(SERVICE_UUID))
        print('After casting SERVICE_UUID to QUuid.')
        bquuid = QBluetoothUuid(quuid)
        print('After casting quuid to a QBluetoothUuid.')
        self.spp_service.setServiceUuid(bquuid)
        print('Set the service\'s UUID!')
        print('Service is complete?', self.spp_service.isComplete())
        print('Service is valid?', self.spp_service.isValid())
        print('Socket protocol:', self.spp_service.socketProtocol())

        # Describe the protocol
        protocols = QBluetoothServiceInfo.Sequence()
        print('Created protocols Sequence.')

        l2cap = QBluetoothServiceInfo.Sequence()
        l2cap.append(QBluetoothUuid(QBluetoothUuid.ProtocolUuid.L2cap))
        print('Created l2cap Sequence.')
        print('Added to l2cap:', l2cap.first())

        rfcomm = QBluetoothServiceInfo.Sequence()
        print('Created rfcomm Sequence.')
        rfcomm.append(QBluetoothUuid(QBluetoothUuid.ProtocolUuid.Rfcomm))
        channel = self.connection_listener_server.serverPort()
        print('RFCOMM channel:', channel)
        rfcomm.append(channel)
        print('rfcomm is now:', rfcomm.toList())

        protocols.append(l2cap)
        protocols.append(rfcomm)
        print('protocols is now:', protocols.toList())

        self.spp_service.setAttribute(
            QBluetoothServiceInfo.AttributeId.ProtocolDescriptorList.value,
            protocols
        )
        print('Set the service\'s ProtocolDescriptorList.')
        print('Is the service now complete?', self.spp_service.isComplete())

        # Register the service
        self.spp_service.registerService(local_address)
        print('Registered Bluetooth service.')
        print('Is the service registered?', self.spp_service.isRegistered())

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