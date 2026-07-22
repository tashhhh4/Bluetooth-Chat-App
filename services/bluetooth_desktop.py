import socket
import subprocess
import logging
from services.bluetooth import BluetoothService
from utils import accept_on_thread

def run_command(*args):
    return subprocess.run([*args], capture_output=True, text=True, check=True).stdout

class DesktopBluetoothService(BluetoothService):

    def __init__(self):

        super().__init__(events=[
            'BONDED_DEVICES_UPDATED',
            'CONNECTION_ESTABLISHED',
            'DISCOVERED_DEVICES_UPDATED',
        ])

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

    def listen_for_connections(self):
        logging.warning('Listen for connections - not yet implemented in DesktopBluetoothService')

        print(self.whats_my_mac_address())

        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

        # accept_on_thread(
        #     sock,
        #     name='Connection Listener',
        #     on_connected=self._handle_connection,
        # )

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

    def _handle_connection(self, sock):
        print('inside _handle_Connection(desktop). sock is', sock)
        self.event_registry.emit_event('CONNECTION_ESTABLISHED', sock)