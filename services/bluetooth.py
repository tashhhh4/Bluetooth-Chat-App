from android.permissions import check_permission, Permission
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
        self.devices.clear()
        self.start_scan()