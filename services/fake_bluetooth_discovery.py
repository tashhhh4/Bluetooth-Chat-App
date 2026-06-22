import logging
from uuid import UUID
import config
from db.manager import settings

# Helper functions
def repr_advertisement(advertisement):
    output = ''
    for ad in advertisement.parse(advertisement.data):
        output += f'TYPE: {ad.ad_type}; LEN: {len(ad.data)}; DATA: {ad.data.hex()}\n'
    return output

def extract_service_uuids(advertisement):
    uuids = []

    for ad in advertisement:

        # 16-bit service UUIDs
        if ad.ad_type in (2, 3):
            print('extracting 16-bit service UUID...')
            data = bytes(ad.data)
            for i in range(0, len(data), 2):
                chunk = data[i:i+2]
                if len(chunk) == 2:
                    value = int.from_bytes(chunk, byteorder='little')
                    uuids.append(
                        UUID(f'0000{value:04x}-0000-1000-8000-00805f9b34fb')
                    )

        # 128-bit service UUIDs
        elif ad.ad_type in (6, 7):
            print('extracting 128-bit service UUID...')
            data = bytes(ad.data)
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                if len(chunk) == 16:
                    uuids.append(UUID(bytes=chunk[::-1]))

    return uuids

EXPLANATION = ' — not implemented in FakeBLEDiscoverer'

class FakeBLEDiscoverer():
    """ BLE Scanning and Advertising Service with most of its functionality removed. """

    SERVICE_UUID = config.SERVICE_UUID
    DEVICE_UUID = None

    def __init__(self):
        super().__init__()

        self.devices = []
        self.advertiser = None

        self.on_device_discovered = None
        self.on_begin_scan = None
        self.on_end_scan = None

        self.DEVICE_UUID = settings.get_device_uuid()

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
