import logging
from utils import EventRegistry, read_input_stream_on_thread

""" A Connection is an object which owns a `connected_socket`.
    It is responsible for running read_input_stream() and send_bytes(),
    but it doesn't need to know what method (Bluetooth) is used to establish the connected_socket.
"""

class Connection:

    def __init__(self, socket_service):
        """ Socket Service must be a class which provides a method like:
                connect_to_device(address) -> connected_socket
        """

        self.socket = None
        self.socket_service = socket_service
        self.socket_service.event_registry.register_event_callback(
            'CONNECTION_ESTABLISHED', self._handle_connection
        )

        self.event_registry = EventRegistry(
            [
                'CONNECTION_ESTABLISHED',
                'CONNECTION_LOST',
                'MESSAGE_RECEIVED',
            ], 'Connection.EventRegistry'
        )

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, value):
        self._socket = value

    def get_remote_name(self):
        return self.socket.getRemoteDevice().name

    def get_remote_address(self):
        return self.socket.getRemoteDevice().address

    def initiate_connection(self, address):
        self.socket_service.connect_to_device(address)

    def send_bytes(self, data):
        if self.socket is None:
            raise IOError('Socket not set.')
        output_stream = self.socket.getOutputStream()
        try:
            output_stream.write(data.encode('utf-8'))
            output_stream.flush()
        except Exception as e:
            logging.warning(f'send_bytes error: {e}')

    def _start_reading_input_stream(self):
        if self.socket is None:
            raise IOError('No connection.')
        input_stream = self.socket.getInputStream()
        read_input_stream_on_thread(
            self.socket,
            input_stream,
            name='Input Stream Reader',
            on_receive=self._handle_receive,
            on_disconnect=self._handle_disconnect,
        )

    def _handle_connection(self, socket):
        self.socket = socket
        self._start_reading_input_stream()
        self.event_registry.emit_event('CONNECTION_ESTABLISHED')

    def _handle_disconnect(self):
        self.socket = None
        self.event_registry.emit_event('CONNECTION_LOST')

    def _handle_receive(self, data):
        logging.debug('[Connection] Running _handle_receive()')
        logging.debug(f'[Connection] Received {data}')
        self.event_registry.emit_event('MESSAGE_RECEIVED', data)
