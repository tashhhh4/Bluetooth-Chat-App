from able import BluetoothDispatcher

class BLE(BluetoothDispatcher):
    """ BLE Service
        Features:
        - Can scan nearby BLE devices and report results.
    """

    def __init__(self):
        super().__init__()

        self.devices = []
        self.on_devices_updated = None

    def scan(self):
        """ Start BLE Scan. """
        print('Starting BLE Scan...')
        self.devices.clear()
        self.start_scan()

    def on_device(self, device, rssi, advertisement):
        """ Called automatically when a device is discovered. """
        print('A device was discovered:', f'{device.getName()} | RSSI <{rssi}> | AD {advertisement}')
        name = device.getName()
        if not name:
            name = 'Unknown device'

        self.devices.append({
            'name': name,
            'rssi': rssi,
            'advertisement': advertisement,
        })

        if self.on_devices_updated:
            self.on_devices_updated(self.devices)

    def on_scan_failed(self, error_code):
        print('BLE scan failed. Error code:', error_code)

    def on_scan_completed(self):
        """ Called when scan finishes. """
        print('BLE scan completed.')
        if self.on_devices_updated:
            self.on_devices_updated(self.devices)