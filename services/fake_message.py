from utils import EventRegistry

class FakeMessageService:

    def __init__(self, bluetooth_service):
        self.event_registry = EventRegistry(['MESSAGE_RECEIVED'])