# Manually edit database entries for Devices and Contacts

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout
from ..utils import add_background, add_rows, fit_height
from db.manager import devices

class DebugDevices(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        # Top-level Page Container
        self.container = BoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Header with Refresh Button
        self.header = BoxLayout(size_hint_y=None, height=50)
        self.refresh_button = Button(text='Refresh Page')
        self.header.add_widget(self.refresh_button)
        self.container.add_widget(self.header)

        # Scrolling Container
        self.scroll_view = ScrollView()
        self.container.add_widget(self.scroll_view)

        # Container inside the scroll
        self.content_container = BoxLayout(orientation='vertical', size_hint_y=None)
        fit_height(self.content_container)
        self.scroll_view.add_widget(self.content_container)

        # Devices Form
        self.devices_form = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=None,
            height=400,
        )
        add_background(self.devices_form, (1, 0, 0, .3))
        self.devices_form_title = Label(text='DEVICES')
        self.devices_form.add_widget(self.devices_form_title)
        self.content_container.add_widget(self.devices_form)

        self.devices_form_name_label = Label(text='Device Name')
        self.devices_form_name_input = TextInput(multiline=False)
        self.devices_form_uuid_label = Label(text='Device UUID')
        self.devices_form_uuid_input = TextInput(multiline=False)
        self.devices_form_address_label = Label(text='Address')
        self.devices_form_address_input = TextInput(multiline=False)
        self.devices_form_contact_label = Label(text='Contact')
        self.devices_form_contact_input = TextInput(multiline=False)
        self.devices_form_button = Button(text='Add', size_hint_x=.8, pos_hint={'center_x': .5})
        self.devices_form.add_widget(self.devices_form_name_label)
        self.devices_form.add_widget(self.devices_form_name_input)
        self.devices_form.add_widget(self.devices_form_uuid_label)
        self.devices_form.add_widget(self.devices_form_uuid_input)
        self.devices_form.add_widget(self.devices_form_address_label)
        self.devices_form.add_widget(self.devices_form_address_input)
        self.devices_form.add_widget(self.devices_form_contact_label)
        self.devices_form.add_widget(self.devices_form_contact_input)
        self.devices_form.add_widget(self.devices_form_button)

        # Devices List
        self.devices_list = GridLayout(
            cols=1,
            row_default_height=50,
            row_force_default=True,
            size_hint_y=None,
        )
        add_background(self.devices_list, (1, 0, 0, .3))
        self.content_container.add_widget(self.devices_list)
        self.populate_devices()

        # Contacts Form
        self.contacts_form = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None, height=170)
        add_background(self.contacts_form, (0, 0, 1, .3))
        self.contacts_form_title = Label(text='CONTACTS')
        self.contacts_form.add_widget(self.contacts_form_title)
        self.content_container.add_widget(self.contacts_form)
        self.contacts_form_name_label = Label(text='Contact Name')
        self.contacts_form_name_input = TextInput(multiline=False)
        self.contacts_form_button = Button(text='Add', size_hint_x=.8, pos_hint={'center_x': .5})
        self.contacts_form.add_widget(self.contacts_form_name_label)
        self.contacts_form.add_widget(self.contacts_form_name_input)
        self.contacts_form.add_widget(self.contacts_form_button)

        # Contacts List
        self.contacts_list = GridLayout(
            cols=1,
            row_default_height=50,
            row_force_default=True,
            size_hint_y=None,
        )
        add_background(self.contacts_list, (0, 0, 1, .3))
        self.content_container.add_widget(self.contacts_list)
        self.populate_contacts()


        # Refresh Button
        def refresh(_):
            self.populate_devices()
            self.populate_contacts()
        self.refresh_button.bind(on_press=refresh)

        # Devices Form Button
        def add_device(_):
            uuid = self.devices_form_uuid_input.text.strip()
            name = self.devices_form_name_input.text.strip()
            address = self.devices_form_address_input.text.strip()
            owner = self.devices_form_owner_input.text.strip()
            devices.create_device(uuid, name, address, owner)

        # Contacts Form Button

    def populate_devices(self):
        self.devices_list.clear_widgets()

        # Add header row
        # col_widths = [20, 50, 90, 20]
        fields = ['uuid', 'name', 'address', 'contact', '']
        data = [fields]
        add_rows(self.devices_list, data, col_widths=None)

        # Get all devices
        # list_ = devices.list_devices()
        list_ = []

        # Add a row for each device
        add_rows(self.devices_list, list_, col_widths=None)

    def populate_contacts(self):
        self.contacts_list.clear_widgets()

        # Add header row
        # col_widths = [30, 150]
        fields = ['id', 'name', '']
        data = [fields]
        add_rows(self.contacts_list, data, col_widths=None)

        # Get all contacts
        list_ = []

        # Add a row for each contact
        add_rows(self.contacts_list, list_, col_widths=None)