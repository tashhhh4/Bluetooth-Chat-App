import threading
import time
from kivy.clock import Clock

def listen(socket, ttl=30, name='socket'):
    try:
        start_time = time.time()
        print(f'Opening listener loop with {name}.')
        while time.time() - start_time < ttl:
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
        name=name + ' thread'
    )
    thread.start()
    return thread

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
