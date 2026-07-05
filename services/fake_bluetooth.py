EXPLANATION = ' — not implemented in FakeBluetoothService'

class FakeBluetoothService:

    discovered_devices = {}
    _callbacks = {
        'DISCOVERED_DEVICES_UPDATED': [],
    }

    @staticmethod
    def scan_for_devices():
        print('Scan for devices' + EXPLANATION)

    @staticmethod
    def stop_scanning():
        print('Stop scanning' + EXPLANATION + ' because scan was never started')

    @staticmethod
    def create_service_listener_socket(ttl):
        print((
                'Open RFcomm Socket with Service Record for '
                + str(ttl) + ' seconds' + EXPLANATION
        ))

    @staticmethod
    def turn_discoverability_on(ttl):
        print((
                'Make this device visible (discoverable) by other Bluetooth'
                ' devices for ' + str(ttl) + ' seconds' + EXPLANATION
        ))

    @staticmethod
    def turn_discovery_on():
        print((
                'Turn discovery mode on using device\'s '
                'default Bluetooth adapter' + EXPLANATION
        ))

    @staticmethod
    def turn_discovery_off():
        print('Turn Bluetooth discovery mode off' + EXPLANATION)

    @staticmethod
    def get_paired_devices():
        print('Get paired Bluetooth devices' + EXPLANATION)
        return []

    def listen_for_service_record(a, b):
        print('Listen for service record' + EXPLANATION)

    def register_event_callback(self, event_name, callback):
        if event_name not in self._callbacks:
            raise TypeError(f'No event called {event_name} for service FakeBluetoothService')
        self._callbacks[event_name].append(callback)