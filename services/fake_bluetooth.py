EXPLANATION = ' — not implemented in FakeBluetoothService'

class FakeBluetoothService:

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