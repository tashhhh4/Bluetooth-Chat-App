""" A Connection is an object which owns a `connected_socket`.
    It is responsible for running read_input_stream() and send_bytes(),
    but it doesn't need to know what method (Bluetooth) is used to establish the connected_socket.
"""

class Connection:

    def __init__(self, socket):
        self.socket = socket