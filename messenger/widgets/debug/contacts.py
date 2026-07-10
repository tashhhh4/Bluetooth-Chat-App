from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from messenger.widgets.utils import (
    add_background,
    bind_height_to_content_height,
    bind_height_to_texture_height,
)
from .components.debug_layout import DebugLayout
from .components.form_field_row import FormFieldRow
from db.manager import contacts as contacts_manager

class DebugContacts(DebugLayout):

    contacts = ListProperty([])

    def __init__(self, **kwargs):
        super(DebugContacts, self).__init__(**kwargs)

        # Contacts Form
        self.contacts_form = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
        )
        bind_height_to_content_height(self.contacts_form)
        self.container.add_widget(self.contacts_form)

        # Contacts Form Title
        self.contacts_form_title = Label(text='CONTACTS')
        bind_height_to_texture_height(self.contacts_form_title)
        self.contacts_form.add_widget(self.contacts_form_title)

        # Contacts Form Name
        self.name_row = FormFieldRow('Contact Name')
        self.contacts_form.add_widget(self.name_row)

        # Contacts Form Button
        self.contacts_form_button = Button(
            text='Add',
            size_hint_x=.8,
            size_hint_y=None,
            height=dp(30),
            pos_hint={'center_x': .5}
        )
        self.contacts_form.add_widget(self.contacts_form_button)

        # Padder
        self.padder = BoxLayout(size_hint_y=None, height=dp(40))
        self.container.add_widget(self.padder)

        # Contacts List Title
        self.contacts_list_title = Label(text='EXISTING RECORDS')
        bind_height_to_texture_height(self.contacts_list_title)
        self.container.add_widget(self.contacts_list_title)

        # Contacts List Header
        self.contacts_list_header = BoxLayout(size_hint_y=None, height=dp(20))
        self.container.add_widget(self.contacts_list_header)

        # Scroller
        self.scroller = ScrollView()
        self.container.add_widget(self.scroller)

        # Contacts List
        self.contacts_list = BoxLayout(orientation='vertical')
        bind_height_to_content_height(self.contacts_list)
        add_background(self.contacts_list, (0, 0, 1, .3))
        self.scroller.add_widget(self.contacts_list)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)

        self.load_contacts()

        ### Bind Actions ###

        # Contacts Form Button
        def add_contact(_):
            name = self.contacts_form_name_input.text.strip()
            contacts_manager.create(name)
        self.contacts_form_button.bind(on_press=add_contact)

    def populate_contacts(self, contacts):
        self.contacts_list.clear_widgets()

        for contact in contacts:
            row = BoxLayout(size_hint_y=None, height=dp(40))
            self.contacts_list.add_widget(row)

            id_value = Label(text=contact.id)
            row.add_widget(id_value)

            name_value = Label(text=contact.name)
            row.add_widget(name_value)

            x_button = Button(text='X')
            def x(_):
                contacts_manager.delete(contact.id)
            row.add_widget(x_button)

    def load_contacts(self):
        self.contacts = contacts_manager.list_contacts()

    def on_contacts(self, _, value):
        self.populate_contacts(value)