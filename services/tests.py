import logging
import unittest
from unittest.mock import patch
from services.bluetooth import BluetoothService
from services.connection import Connection
from services.message import MessageService, MessageObject, Message
from services.platform import ListHandler
from utils import EventRegistry

HIDE_LOGS = True

def get_logs_with(logs, terms):
    logs = logs[:]
    for t in terms:
        logs = [l for l in logs if t in l]
    return logs

class PretendSocket:
    def getInputStream(self):
        return None

class ServiceTests(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()

        self.console_handler = next(h for h in logger.handlers if h.__class__.__name__ == 'ConsoleHandler')
        if HIDE_LOGS:
            logger.removeHandler(self.console_handler)

        self.list_in_memory_handler = ListHandler()
        self.list_in_memory_handler.setFormatter(
            logging.Formatter('[TEST] [%(levelname)s] [%(asctime)s] %(message)s')
        )
        logger.addHandler(self.list_in_memory_handler)
        self.logs = self.list_in_memory_handler.logs

    def tearDown(self):
        logger = logging.getLogger()
        logger.removeHandler(self.list_in_memory_handler)
        if HIDE_LOGS:
            logger.addHandler(self.console_handler)

    def assertLogContains(self, *terms):
        """ Passes if any log in self.logs contains all of the terms. """
        logs = get_logs_with(self.logs, terms)
        if not logs:
            raise AssertionError(f'No logs found containing {terms}')

    def assertLogComesAfter(self, terms1, terms2):
        """ Passes if the first log containing all of terms1 comes before
            the first log containing all of terms2 in self.logs .
        """
        logs1 = get_logs_with(self.logs, terms1)
        logs2 = get_logs_with(self.logs, terms2)
        if not logs1:
            raise AssertionError(f'No logs found containing {terms1}')
        if not logs2:
            raise AssertionError(f'No logs found containing {terms2}')
        index1 = self.logs.index(logs1[0])
        index2 = self.logs.index(logs2[0])
        if not index1 < index2:
            raise AssertionError(f'Failed to find log containing {terms1} before {terms2}.')

    def assertLogsInOrder(self, *term_sets):
        """ This function may receive any number of tuples representing search terms for logs.
            It will pass if the first log containing each set of terms comes before the next one
            in self.logs. The argument is called 'term_sets' but it should be a list or a tuple.
        """
        last_index = 0
        for terms in term_sets:
            logs = get_logs_with(self.logs, terms)
            if not logs:
                raise AssertionError(f'No logs found containing {terms}')
            hit_index = self.logs.index(logs[0])
            if not hit_index > last_index:
                raise AssertionError((
                    f'Logs not in expected order\nlast (i={last_index}): {self.logs[last_index]}\n'
                    'current (i={hit_index}): {self.logs[hit_index]}'
                ))

    # Tests

    def test_bluetooth_service_initialized(self):
        bluetooth_service = BluetoothService()
        self.assertHasAttr(bluetooth_service, 'event_registry')
        self.assertIsInstance(bluetooth_service.event_registry, EventRegistry)
        for event in ['BONDED_DEVICES_UPDATED', 'CONNECTION_ESTABLISHED', 'DISCOVERED_DEVICES_UPDATED']:
            self.assertIn(event, bluetooth_service.event_registry._callbacks.keys())

    def test_connection_initialized(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)
        self.assertIsNone(connection.socket)
        self.assertIsInstance(connection.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)
        connection._handle_disconnect()
        self.assertIn('CONNECTION_LOST', self.logs[-1])

    def test_connection_io_errors(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)
        with self.assertRaises(IOError):
            connection._start_reading_input_stream()
        with self.assertRaises(IOError):
            connection.send_bytes('data')

    def test_message_service_initialized(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)
        message_service = MessageService(connection)
        self.assertHasAttr(message_service, 'connection')
        self.assertIsInstance(message_service.connection, Connection)

    def test_bluetooth_service_and_connection_event_timing(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)

        # bluetooth_service passes a socket into its _handle_connection,
        # connection emits event,
        # then bluetooth_service emits event.
        pretend_socket = PretendSocket()
        with patch.object(connection, '_start_reading_input_stream'):
            bluetooth_service._handle_connection(pretend_socket)
        self.assertIs(connection.socket, pretend_socket)
        self.assertLogComesAfter(
            ('BluetoothService.EventRegistry', 'CONNECTION_ESTABLISHED'),
            ('Connection.EventRegistry', 'CONNECTION_ESTABLISHED'),
        )

    def test_connection_and_message_service_event_timing(self):
        bluetooth_service = BluetoothService()
        connection = Connection(bluetooth_service)
        MessageService(connection)

        # connection emits after disconnect occurs,
        # then message_service emits disconnect event
        connection._handle_disconnect()
        self.assertLogComesAfter(
            ('Connection.EventRegistry', 'CONNECTION_LOST'),
            ('MessageService.EventRegistry', 'DEVICE_DISCONNECTED'),
        )

        # connection emits MESSAGE_RECEIVED,
        # then message_service emits MESSAGE_RECEIVED
        message = MessageObject(Message('test'), sender_uuid='12345', role='message')
        data = message.to_json()
        try:
            connection._handle_receive(data)
        except RuntimeError:
            pass
        self.assertLogsInOrder(
            ('Connection', 'Received', 'test'),
            ('Connection.EventRegistry', 'MESSAGE_RECEIVED'),
            ('MessageService', '_handle_message_received')
        )
