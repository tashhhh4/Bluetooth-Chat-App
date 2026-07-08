import logging
import threading
import time
from kivy.clock import Clock

def listen(socket, ttl=30, name='socket'):
    try:
        start_time = time.time()
        print(f'Opening listener loop with {name}.')
        while True:
            if ttl != 0 and time.time() - start_time < ttl:
                break

            try:
                client = socket.accept(1000)  # 1 second timeout
                print(f'Connection accepted on {name}.')
                client.close()
            except Exception as e:
                print(e)
        print(f'{name.capitalize()} loop closed after time limit.')
    finally:
        socket.close()
        print(f'{name.capitalize()} closed.')

def listen_on_thread(socket, ttl=30, name='socket'):
    """ Creates a thread that runs `listen` with the desired parameters.
        Returns the new active thread.
    """
    thread = threading.Thread(
        target=listen,
        args=(socket, ttl, name),
        daemon=True,
        name=name + ' thread',
    )
    thread.start()
    return thread

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

    logging.info('Running connect()')
    try:
        while True:
            try:
                socket.connect()
                logging.info('Connection established.')
                if on_connected:
                    on_connected(socket)
                break
            except JavaException as j:
                print('No connection yet.')
            except Exception as e:
                print('Connect Error:', e)
    except Exception as e:
        print(e)

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

def read_input_stream(connected_socket, input_stream, name='input stream receiver', on_receive=None):
    buffer = bytearray(1024)
    while connected_socket:
        try:
            bytes_read = input_stream.read(buffer)
            if bytes_read > 0:
                data = buffer[:bytes_read].decode('utf-8')
                if on_receive:
                    on_receive(data)
        except Exception as e:
            print('Read Input Stream Error:', e)
            break

def read_input_stream_on_thread(connected_socket, input_stream, name='input stream receiver', on_receive=None):
    """ Creates a thread to run `receive_and_read`.
        Returns the new active thread.
    """
    thread = threading.Thread(
        target=read_input_stream,
        args=(connected_socket, input_stream, name, on_receive),
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

    def emit_event(self, event_name, *args, **kwargs):
        """ Calls all the functions at _callbacks[event_name], with arguments if applicable. """
        for callback in self._callbacks[event_name]:
            callback(*args, **kwargs)

    def _add_event(self, event_name):
        """ Adds a new key (event_name) and value (empty list) to _callbacks dictionary. """
        self._callbacks[event_name] = []