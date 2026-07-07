import logging
import inspect

class Service:
    class_name = ""
    def __init__(self):
        self.class_name = self.__class__.__name__

    def log_info(self, message, *args, **kwargs):
        logging.info(f'[{self.class_name}][{inspect.currentframe().f_back.f_code.co_name}] {message}', args, kwargs)