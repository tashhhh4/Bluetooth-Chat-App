import socket
import subprocess
import logging
from utils import accept_on_thread

from services.bluetooth import BluetoothService

class DesktopBluetoothService(BluetoothService):

    def __init__(self):

        super().__init__(events=[
            'BONDED_DEVICES_UPDATED',
            'CONNECTION_ESTABLISHED',
            'DISCOVERED_DEVICES_UPDATED',
        ])

    def listen_for_connections(self):
        logging.warning('Listen for connections - not yet implemented in DesktopBluetoothService')

        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

        # accept_on_thread(
        #     sock,
        #     name='Connection Listener',
        #     on_connected=self._handle_connection,
        # )

    def load_paired_devices(self):
        logging.warning('Load Paired Devices - not yet implemented in DesktopBluetoothService')

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

    def _handle_connection(self, sock):
        print('inside _handle_Connection(desktop). sock is', sock)
        self.event_registry.emit_event('CONNECTION_ESTABLISHED', sock)