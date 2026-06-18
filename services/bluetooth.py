from uuid import UUID
from able import BluetoothDispatcher
from able.advertising import (
    Advertiser,
    AdvertiseData,
    Interval,
    ServiceUUID,
    TXPower,
)

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
            data = bytes(ad.data)
            for i in range(0, len(data), 2):
                chunk = data[i:i+2]
                if len(chunk) == 2:
                    value = int.from_bytes(chunk, byteorder='little')
                    uuids.append(
                        f'0000{value:04x}-0000-1000-8000-00805f9b34fb'
                    )

        # 128-bit service UUIDs
        elif ad.ad_type in (6, 7):
            data = bytes(ad.data)
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                if len(chunk) == 16:
                    uuids.append(str(UUID(bytes_le=chunk)))

    return uuids

class BLE(BluetoothDispatcher):
    """ BLE Service
        Features:
        - Can scan nearby BLE devices and save them to a list.
        - Can advertise Blu2's service UUID.
    """

    def __init__(self):
        super().__init__()

        self.devices = []
        self.advertiser = None

        self.on_device_discovered = None
        self.on_begin_scan = None
        self.on_end_scan = None

    def start_advertising(self):
        """ Start advertising Blu2's BLE service. """
        service_uuid = settings.get_service_uuid()
        print('Starting BLE advertisement with service UUID', service_uuid)
        data = AdvertiseData(ServiceUUID(service_uuid))
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
            RSSI: Signal strength indicator.
        """
        name = device.getName()
        if not name:
            name = 'Unknown device'

        address = device.getAddress()

        service_uuids = extract_service_uuids(advertisement)

        if not self.device_already_discovered(device):
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