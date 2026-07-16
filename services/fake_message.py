from utils import EventRegistry

class FakeMessageService:

    def __init__(self, connection, bluetooth_service):
        self.event_registry = EventRegistry(['MESSAGE_RECEIVED'])
        self.connection = connection
        self.bluetooth_service = bluetooth_service