from able import BluetoothDispatcher
from able.advertising import (
    Advertiser,
    AdvertiseData,
    ManufacturerData,
    Interval,
    ServiceUUID,
    TXPower,
    TXPowerLevel,
)

from db.manager import settings

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

        if not self.device_already_discovered(device):
            self.devices.append({
                'name': name,
                'address': address,
                'signal': rssi,
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