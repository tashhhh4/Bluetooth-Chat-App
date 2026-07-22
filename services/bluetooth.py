from abc import abstractmethod, ABCMeta
from services.service import Service

class BluetoothService(Service, metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def listen_for_connections(self):
        pass