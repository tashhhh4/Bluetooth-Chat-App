from utils import EventRegistry

class Service:

    def __init__(self, events):

        self.event_registry = EventRegistry(events, f'{self.__class__.__name__}.{EventRegistry.__name__}')
