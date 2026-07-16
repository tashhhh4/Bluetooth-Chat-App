import logging
from utils import EventRegistry

""" A Connection is an object which owns a `connected_socket`.
    It is responsible for running read_input_stream() and send_bytes(),
    but it doesn't need to know what method (Bluetooth) is used to establish the connected_socket.
"""

class Connection:

    def __init__(self, socket):

        self.event_registry = EventRegistry(
            [
                'CONNECTION_ESTABLISHED',
                'CONNECTION_LOST',
                'MESSAGE_RECEIVED',
            ], 'Connection.EventRegistry'
        )

        self.first_initialization = True
        self.socket = socket

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, value):
        self._socket = value
        if value is None:
            if self.first_initialization:
                self.first_initialization = False
                return
            self.event_registry.emit_event('CONNECTION_LOST')
        else:
            self.event_registry.emit_event('CONNECTION_ESTABLISHED')

    def send_bytes(self, data):
        if self.socket is None:
            raise IOError('Socket not set.')
        output_stream = self.socket.getOutputStream()
        try:
            output_stream.write(data.encode('utf-8'))
            output_stream.flush()
        except Exception as e:
            logging.warning(f'send_bytes error: {e}')