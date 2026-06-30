from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from messenger.widgets.debug.components.debug_layout import DebugLayout
from messenger.widgets.utils import fit_height

# TEMP BACKEND
# Todo: move this stuff out of the frontend
from config import SERVICE_UUID
from config import ENVIRONMENT
if ENVIRONMENT == 'debug':
    from pprint import pprint
    import threading
    from jnius import autoclass
    JavaUUID = autoclass('java.util.UUID')
    java_uuid = JavaUUID.fromString(str(SERVICE_UUID))
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    adapter = BluetoothAdapter.getDefaultAdapter()
    server = adapter.listenUsingRfcommWithServiceRecord('Blu2', java_uuid)

    def listen():
        conn = server.accept()
        print('Created a connection. Connection is:', conn)
        print('type:', type(conn))
        print('dir:')
        pprint(dir(conn))

    def connect():
        print('Running connect.')
        device = adapter.getRemoteDevice('AA:BB:CC:DD:EE:FF')
        print('About the device...')
        print('ACCESS_ALLOWED:', device.ACCESS_ALLOWED)
        print('ACCESS_REJECTED:', device.ACCESS_REJECTED)
        print('ACCESS_UNKNOWN:', device.ACCESS_UNKNOWN)
        print('CONNECTION_ACCESS_NO:', device.CONNECTION_ACCESS_NO)
        print('CONNECTION_ACCESS_YES:', device.CONNECTION_ACCESS_YES)
        print('CREATOR:', device.CREATOR)
        print('DEVICE_TYPE_HEADSET:', device.DEVICE_TYPE_HEADSET)
        print('DEVICE_TYPE_UNKNOWN:', device.DEVICE_TYPE_UNKNOWN)
        print('ERROR:', device.ERROR)
        print('METADATA_DEVICE_TYPE:', device.METADATA_DEVICE_TYPE)
        print('PAIRING_VARIANT_CONSENT:', device.PAIRING_VARIANT_CONSENT)
        print('BOND_BONDED:', device.BOND_BONDED)
        print('BOND_BONDING:', device.BOND_BONDING)
        print('BOND_LOSS_REASON_BREDR_AUTH_FAILURE:', device.BOND_LOSS_REASON_BREDR_AUTH_FAILURE)
        print('BOND_LOSS_REASON_BREDR_INCOMING_PAIRING:', device.BOND_LOSS_REASON_BREDR_INCOMING_PAIRING)
        print('BOND_LOSS_REASON_LE_ENCRYPT_FAILURE:', device.BOND_LOSS_REASON_LE_ENCRYPT_FAILURE)
        print('BOND_LOSS_REASON_LE_INCOMING_PAIRING:', device.BOND_LOSS_REASON_LE_INCOMING_PAIRING)
        print('BOND_LOSS_REASON_UNKNOWN:', device.BOND_LOSS_REASON_UNKNOWN)
        print('BOND_NONE:', device.BOND_NONE)
        print('bond state:', device.getBondState())
        print('is connected:', device.isConnected())
        print('name:', device.name)


    def start_thread():
        threading.Thread(target=listen, daemon=True).start()
        print('Started thread.')

    def send(address, message):
        pass

    def recv():
        pass

    # Try it out
    start_thread()
    connect()

class DebugTransport(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugTransport, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', padding=10, spacing=20)
        self.add_widget(self.container)

        # Page Title
        self.title = Label(text='Transport', font_size=24, size_hint_y=None, height=40)
        self.container.add_widget(self.title)

        # Device UUID
        self.device_info = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        fit_height(self.device_info)
        self.container.add_widget(self.device_info)

        # Label
        self.device_uuid_label = Label(text='Recipient Device UUID', size_hint_y=None, height=30)
        self.device_info.add_widget(self.device_uuid_label)

        # Input
        self.device_uuid_input = TextInput(size_hint_y=None, height=50)
        self.device_info.add_widget(self.device_uuid_input)

        # SEND Button
        self.send_button = Button(
            text='SEND',
            background_color='yellow',
            size_hint_y=None,
            height=50,
            size_hint_x=.6,
            pos_hint={'center_x': .5},
        )
        self.container.add_widget(self.send_button)

        # SEND Button tooltip
        self.send_button_tooltip = Label(text='Sends "Hello World".', font_size=14, size_hint_y=None, height=30)
        self.container.add_widget(self.send_button_tooltip)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)