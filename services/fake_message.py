from utils import EventRegistry

class FakeMessageService:

    event_registry = EventRegistry(['MESSAGE_RECEIVED'])

    def __init__(self, bluetooth_service):
        pass