# Manually edit database entries for Devices and Contacts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout
from ..utils import add_background, add_rows

class DebugDevices(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        # Top-level Page Wrapper
        self.container = BoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Header with Refresh Button
        self.header = BoxLayout(size_hint_y=.1)
        self.refresh_button = Button(text='Refresh Page')
        self.header.add_widget(self.refresh_button)
        self.container.add_widget(self.header)

        # Devices
        self.devices_container = BoxLayout(size_hint_y=.5)
        self.container.add_widget(self.devices_container)

        # Devices Form
        self.devices_form = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.devices_form_title = Label(text='DEVICES')
        self.devices_form.add_widget(self.devices_form_title)
        self.devices_container.add_widget(self.devices_form)

        self.devices_form_name_label = Label(text='Device Name')
        self.devices_form_name_input = TextInput(multiline=False)
        self.devices_form_address_label = Label(text='Address')
        self.devices_form_address_input = TextInput(multiline=False)
        self.devices_form_button = Button(text='Add', size_hint_x=.8, pos_hint={'center_x': .5})
        self.devices_form.add_widget(self.devices_form_name_label)
        self.devices_form.add_widget(self.devices_form_name_input)
        self.devices_form.add_widget(self.devices_form_address_label)
        self.devices_form.add_widget(self.devices_form_address_input)
        self.devices_form.add_widget(self.devices_form_button)

        # Devices List
        self.devices_list = GridLayout(cols=1, row_default_height=50, row_force_default=True)
        add_background(self.devices_list, (1, 0, 0, .3))
        self.devices_container.add_widget(self.devices_list)
        # Devices List Header
        col_widths = [20, 50, 90, 20]
        fields = ['id', 'name', 'address', 'c']
        data = [fields]
        add_rows(self.devices_list, data, col_widths=col_widths)

        # Contacts
        self.contacts_container = BoxLayout(size_hint_y=.5)
        self.container.add_widget(self.contacts_container)

        # Contacts Form
        self.contacts_form = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.contacts_form_title = Label(text='CONTACTS')
        self.contacts_form.add_widget(self.contacts_form_title)
        self.contacts_container.add_widget(self.contacts_form)
        self.contacts_form_name_label = Label(text='Contact Name')
        self.contacts_form_name_input = TextInput(multiline=False)
        self.contacts_form_button = Button(text='Add', size_hint_x=.8, pos_hint={'center_x': .5})
        self.contacts_form.add_widget(self.contacts_form_name_label)
        self.contacts_form.add_widget(self.contacts_form_name_input)
        self.contacts_form.add_widget(self.contacts_form_button)

        # Contacts List
        self.contacts_list = GridLayout(cols=1, row_default_height=50, row_force_default=True)
        add_background(self.contacts_list, (0, 0, 1, .3))
        self.contacts_container.add_widget(self.contacts_list)
        # Contacts List Header
        col_widths = [30, 150]
        fields = ['id', 'name']
        data = [fields]
        add_rows(self.contacts_list, data, col_widths=col_widths)