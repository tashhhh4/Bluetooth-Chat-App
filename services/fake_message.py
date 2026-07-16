from utils import EventRegistry

class FakeMessageService:

    def __init__(self, connection):
        self.event_registry = EventRegistry(['MESSAGE_RECEIVED'])
        self.connection = connection
