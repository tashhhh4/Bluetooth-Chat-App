# Manually edit database entries for Device

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from .components.cell import Cell
from .components.debug_layout import DebugLayout
from .components.form_field_row import FormFieldRow
from messenger.widgets.utils import (
    bind_height_to_content_height,
    bind_height_to_texture_height,
    wrap_text,
)
from db.manager import devices as devices_manager

class DebugDevices(DebugLayout):

    devices = ListProperty([])

    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        # Top-level Page Container
        self.container = BoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Refresh Button
        self.refresh_button = Button(text='Refresh Page', size_hint_y=None, height=dp(40))
        self.container.add_widget(self.refresh_button)

        # Devices Form
        self.devices_form = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
        )
        bind_height_to_content_height(self.devices_form)
        self.container.add_widget(self.devices_form)

        # Devices Form Title
        self.devices_form_title = Label(text='DEVICES')
        bind_height_to_texture_height(self.devices_form_title)
        self.devices_form.add_widget(self.devices_form_title)

        # Devices Form Name
        self.name_row = FormFieldRow('Device Name')
        self.devices_form.add_widget(self.name_row)

        # Devices Form UUID
        self.uuid_row = FormFieldRow('Device UUID')
        self.devices_form.add_widget(self.uuid_row)

        # Devices Form Address
        self.address_row = FormFieldRow('Address')
        self.devices_form.add_widget(self.address_row)

        # Devices Form Contact
        self.contact_row = FormFieldRow('Contact')
        self.contact_row.label.color = (.8, .8, .8, 1)
        self.contact_row.input.disabled = True
        self.devices_form.add_widget(self.contact_row)

        # Devices Form Submit Button
        self.devices_form_button = Button(
            text='Add',
            size_hint_x=.8,
            size_hint_y=None,
            height=dp(30),
            pos_hint={'center_x': .5}
        )
        self.devices_form.add_widget(self.devices_form_button)

        # Padder
        self.padder = BoxLayout(size_hint_y=None, height=dp(20))
        self.container.add_widget(self.padder)

        # Devices List
        self.devices_list_container = BoxLayout(orientation='vertical', spacing=dp(5))
        self.container.add_widget(self.devices_list_container)

        # Devices List Title
        self.devices_list_title = Label(text='EXISTING RECORDS')
        bind_height_to_texture_height(self.devices_list_title)
        self.devices_list_container.add_widget(self.devices_list_title)

        # Devices List Header Row
        self.devices_list_header = BoxLayout(size_hint_y=None, height=dp(20))
        self.devices_list_container.add_widget(self.devices_list_header)

        # Header Row cols
        self.uuid_header = Label(text='uuid')
        self.devices_list_header.add_widget(self.uuid_header)
        self.name_header = Label(text='name')
        self.devices_list_header.add_widget(self.name_header)
        self.address_header = Label(text='address')
        self.devices_list_header.add_widget(self.address_header)
        self.x_button_header = Label()
        self.devices_list_header.add_widget(self.x_button_header)

        # Scroller
        self.scroller = ScrollView()
        self.devices_list_container.add_widget(self.scroller)

        # Devices List Records
        self.devices_list = BoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.devices_list)
        self.scroller.add_widget(self.devices_list)

        ### Bind Actions ###

        # Refresh Button
        self.refresh_button.bind(on_press=lambda _: self.load_devices())

        # Devices Form Button
        def add(_):
            uuid = self.uuid_row.input.text.strip()
            name = self.name_row.input.text.strip()
            address = self.address_row.input.text.strip()
            self.uuid_row.input.text = ''
            self.name_row.input.text = ''
            self.address_row.input.text = ''
            devices_manager.create(uuid, name, address)
            self.load_devices()
        self.devices_form_button.bind(on_press=add)

    def populate_devices(self, devices):
        self.devices_list.clear_widgets()
        for device in devices:
            row = BoxLayout(height=dp(50), size_hint_y=None, spacing=dp(2))
            self.devices_list.add_widget(row)

            uuid_cell = Cell(text=device.uuid)
            row.add_widget(uuid_cell)

            name = device.name if device.name else 'None'
            name_cell = Cell(text=name)
            row.add_widget(name_cell)

            address = device.address if device.address else 'None'
            address_cell = Cell(text=address)
            row.add_widget(address_cell)

            x_button = Button(text='X')
            def x(_):
                devices_manager.delete(device.uuid)
                self.load_devices()
            x_button.bind(on_press=x)
            row.add_widget(x_button)

    def load_devices(self):
        devices = devices_manager.list_devices()
        self.populate_devices(devices)

    def on_pre_enter(self):
        self.load_devices()