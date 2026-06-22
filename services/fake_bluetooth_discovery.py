import logging

EXPLANATION = ' — not implemented in FakeBLEScanner'

class FakeBLEScanner():
    """ BLE Scanning and Advertising Service with most of its functionality removed. """

    def __init__(self):
        super().__init__()

    def start_advertising(self):
        logging.info('Start BLE Advertising' + EXPLANATION)

    def stop_advertising(self):
        logging.info('Stop BLE Advertisement' + EXPLANATION)

    def scan(self):
        logging.info('Scan' + EXPLANATION)

    def stop(self):
        logging.info('Stop' + EXPLANATION)

    def on_device(self, device, rssi, advertisement):
        pass

    def device_already_discovered(self, device):
        pass

    def on_scan_failed(self, error_code):
        pass

    def on_scan_completed(self):
        pass
