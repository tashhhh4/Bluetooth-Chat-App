import logging
from services.service import Service

class FakeMessageService(Service):

    def __init__(self, connection):

        super().__init__(events=['MESSAGE_RECEIVED'])

        self.connection = connection

    def load_chats(self):
        logging.info('Load Chat - Not Implemented in Fake Message Service')
        return []