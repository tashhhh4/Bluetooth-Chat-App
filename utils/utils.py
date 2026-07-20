import logging
import threading
import unittest
from kivy.clock import Clock

def accept(socket, name='accept socket', on_connected=None):
    logging.info('Running accept()')
    try:
        connected = False
        while not connected:
            try:
                client = socket.accept()
                if on_connected:
                    on_connected(client)
                connected = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def accept_on_thread(socket, name='accept socket', on_connected=None):
    """ Creates a thread that runs `accept` with the desired parameters.
        Returns the new active thread.
    """
    thread = threading.Thread(
        target=accept,
        args=(socket, name, on_connected),
        daemon=True,
        name=name + ' thread',
    )
    thread.start()
    return thread

def connect(socket, name='connector socket', on_connected=None):
    from jnius import JavaException

    logging.info(f'Running connect() with {name}.')
    try:
        while True:
            try:
                socket.connect()
                logging.info('Connection established.')
                if on_connected:
                    on_connected(socket)
                break
            except JavaException as j:
                logging.info('No connection yet.')
            except Exception as e:
                logging.error(f'Connect Error: {e}')
    except Exception as e:
        logging.error(str(e))
    finally:
        logging.info(f'Stopped running connect() on {name}.')

def connect_on_thread(socket, name='connector socket', on_connected=None):
    """ Creates a thread that runs `connect`.
        Returns the new active thread.
    """
    thread = threading.Thread(
        target=connect,
        args=(socket, name, on_connected),
        daemon=True,
        name=name + ' thread',
    )
    thread.start()
    return thread

def read_input_stream(
    connected_socket,
    input_stream,
    name='input stream receiver',
    on_receive=None,
    on_disconnect=None
):
    buffer = bytearray(1024)

    try:
        while True:
            bytes_read = input_stream.read(buffer)

            if bytes_read == -1:
                logging.info('read_input_stream(): Input Stream closed.')
                break

            if bytes_read > 0:
                data = buffer[:bytes_read].decode('utf-8')
                if on_receive:
                    on_receive(data)

    except Exception as e:
        print('Read Input Stream Error:', e)

    finally:
        try:
            connected_socket.close()
        except Exception:
            pass

        if on_disconnect:
            on_disconnect()

def read_input_stream_on_thread(connected_socket, input_stream, name='input stream receiver', on_receive=None, on_disconnect=None):
    """ Creates a thread to run `receive_and_read`.
        Returns the new active thread.
    """
    thread = threading.Thread(
        target=read_input_stream,
        args=(connected_socket, input_stream, name, on_receive, on_disconnect),
        daemon=True,
        name=name + ' thread',
    )
    thread.start()
    return thread

def device_java_obj_to_dict(device_obj):
    """ Converts a BluetoothDevice from the Android Bluetooth API into a dictionary."""
    return {'name': device_obj.name, 'address': device_obj.address}

def pluralize(text, number):
    if number == 1:
        return text
    return text + 's'

def schedule(func):
    """ Wrapper for Kivy.clock.Clock.schedule_once, because
        I find the name confusing.
    """
    Clock.schedule_once(func)

def repr_advertisement(advertisement):
    """ Prints out the details of an Advertisement (able library) from a BLE device scan. """
    output = ''
    for ad in advertisement.parse(advertisement.data):
        output += f'TYPE: {ad.ad_type}; LEN: {len(ad.data)}; DATA: {ad.data.hex()}\n'
    return output

class EventRegistry:
    def __init__(self, event_names, name='EventRegistry'):
        self.name = name
        self._callbacks = {}
        for name in event_names:
            self._add_event(name)

    def register_event_callback(self, event_name, callback):
        if event_name not in self._callbacks:
            raise TypeError(f'No event called {event_name} in {self.name}')
        self._callbacks[event_name].append(callback)

    def unregister_event_callback(self, event_name, callback):
        if event_name not in self._callbacks:
            raise TypeError(f'No event called {event_name} in {self.name}')
        self._callbacks[event_name].remove(callback)

    def emit_event(self, event_name, *args, **kwargs):
        """ Calls all the functions at _callbacks[event_name], with arguments if applicable. """
        logging.debug(f'[{self.name}] emits {event_name}')
        for callback in self._callbacks[event_name]:
            callback(*args, **kwargs)

    def _add_event(self, event_name):
        """ Adds a new key (event_name) and value (empty list) to _callbacks dictionary. """
        self._callbacks[event_name] = []

HIDE_LOGS = True

class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))

def get_logs_with(logs, terms):
    logs = logs[:]
    for t in terms:
        logs = [l for l in logs if t in l]
    return logs

class TestSuite(unittest.TestCase):

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