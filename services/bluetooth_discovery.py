from uuid import UUID
from able import BluetoothDispatcher
from able.advertising import (
    Advertiser,
    AdvertiseData,
    Interval,
    ServiceUUID,
    TXPower,
)
import config
from db.manager import settings

# Helper functions
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

class BLEScanner(BluetoothDispatcher):
    """ BLE Scanning and Advertising Service
        Features:
        - Can advertise Blu2's service UUID.
        - Can scan and identify nearby BLE devices which are advertising Blu2's service UUID.
    """

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
        """ Start advertising Blu2's BLE service. """
        print('Starting BLE advertisement with service UUID', self.SERVICE_UUID)
        data = AdvertiseData(ServiceUUID(str(self.SERVICE_UUID)))
        self.advertiser = Advertiser(
            ble=self,
            data=data,
            interval=Interval.MEDIUM,
            tx_power=TXPower.MEDIUM,
        )
        self.advertiser.start()

    def stop_advertising(self):
        """ Stop BLE advertising. """
        print('Stopping BLE advertisement.')
        if self.advertiser:
            self.advertiser.stop()
            self.advertiser = None

    def scan(self):
        """ Start BLE Scan. """
        print('Starting BLE Scan...')

        self.devices.clear()
        self.start_scan()
        if self.on_begin_scan:
            self.on_begin_scan()

    def stop(self):
        """ Stops BLE Scanning. """
        print('Stopping BLE Scan.')
        self.stop_scan()
        if self.on_end_scan:
            self.on_end_scan()

    def on_device(self, device, rssi, advertisement):
        """ Called automatically when a device is discovered.
            device: object representing basic device info - name, address
            rssi: Signal strength indicator.
            advertisement: A tiny packet of data
        """
        name = device.getName()
        if not name:
            name = 'Unknown device'

        address = device.getAddress()

        if self.device_already_discovered(device):
            return

        service_uuids = extract_service_uuids(advertisement)

        if not service_uuids:
            return

        if self.SERVICE_UUID not in service_uuids:
            return

        uuid_list = ', '.join(str(u) for u in service_uuids)
        print(f'Device found: {address} ({name}) | Service UUIDs: {uuid_list}')

        self.devices.append({
            'name': name,
            'address': address,
            'signal': rssi,
            'service_uuids': service_uuids,
        })

        if self.on_device_discovered:
            self.on_device_discovered(self.devices)

    def device_already_discovered(self, device):
        address = device.getAddress()
        for existing_device in self.devices:
            if existing_device['address'] == address:
                return True
        return False

    def on_scan_failed(self, error_code):
        print('BLE scan failed. Error code:', error_code)

    def on_scan_completed(self):
        """ Called when scan finishes. """
        print('BLE scan completed.')
