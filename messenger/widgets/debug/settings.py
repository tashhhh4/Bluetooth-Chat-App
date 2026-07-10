from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from messenger.widgets.utils import bind_height_to_content_height, wrap_text
from .components.debug_layout import DebugLayout
import config
from db.manager import settings

class UuidCell(BoxLayout):

    value = StringProperty('')

    def __init__(self, value, **kwargs):

        self.value = value

        super(UuidCell, self).__init__(**kwargs)

        self.label = Label(text=self.value)
        wrap_text(self.label)
        self.add_widget(self.label)

    def on_value(self, _, value):
        print('inside this UuidCell object. My value was changed. It should be', value)
        self.label.text = value

class DebugSettings(DebugLayout):

    def __init__(self, **kwargs):
        super(DebugSettings, self).__init__(**kwargs)

        # Top-level Container
        self.container = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.add_widget(self.container)

        # Refresh Button
        self.refresh_button = Button(text='Refresh Page', size_hint_y=None, height=dp(50))
        self.container.add_widget(self.refresh_button)

        # Config Chart Title
        self.config_chart_title = Label(text='Settings Loaded from Config', size_hint_y=None, height=dp(30))
        self.container.add_widget(self.config_chart_title)

        # Config Settings
        self.config_settings_container = BoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.config_settings_container)
        self.container.add_widget(self.config_settings_container)

        # Header Row
        self.config_row_0 = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(30))
        self.config_settings_container.add_widget(self.config_row_0)
        self.key_label = Label(text='KEY', size_hint_x=.3)
        self.config_row_0.add_widget(self.key_label)
        self.value_label = Label(text='VALUE')
        self.config_row_0.add_widget(self.value_label)

        # SERVICE_UUID
        self.config_row_1 = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        self.config_settings_container.add_widget(self.config_row_1)
        self.service_uuid_label = Label(text='SERVICE UUID', size_hint_x=.3)
        self.config_row_1.add_widget(self.service_uuid_label)
        self.service_uuid_cell = UuidCell(value='loading')
        self.config_row_1.add_widget(self.service_uuid_cell)

        # Settings Stored in Database
        self.db_settings_container = BoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.db_settings_container)
        self.container.add_widget(self.db_settings_container)

        # Header Row
        self.db_row_0 = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(30))
        self.db_settings_container.add_widget(self.db_row_0)
        self.db_key_label = Label(text='KEY', size_hint_x=.3)
        self.db_row_0.add_widget(self.db_key_label)
        self.db_value_label = Label(text='VALUE')
        self.db_row_0.add_widget(self.db_value_label)
        self.db_empty_widget = Widget(size_hint_x=.2)
        self.db_row_0.add_widget(self.db_empty_widget)


        # DEVICE_UUID
        self.db_row_1 = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        self.db_settings_container.add_widget(self.db_row_1)
        self.device_uuid_key = Label(text='DEVICE_UUID', size_hint_x=.3)
        self.db_row_1.add_widget(self.device_uuid_key)
        self.device_uuid_cell = UuidCell(value='loading')
        self.db_row_1.add_widget(self.device_uuid_cell)
        self.device_uuid_x_button = Button(text='Delete', size_hint_x=.2)
        self.db_row_1.add_widget(self.device_uuid_x_button)

        # Spacer

        self.spacer = Widget()
        self.container.add_widget(self.spacer)

        ### Bind Action ###

        # Refresh Page
        def refresh_page(_):
            self.load_settings()
        self.refresh_button.bind(on_press=refresh_page)

        # Delete Device UUID
        def delete_device_uuid(_):
            settings.delete('DEVICE_UUID')
            self.load_settings()
        self.device_uuid_x_button.bind(on_press=delete_device_uuid)

    def load_settings(self):
        service_uuid = str(config.SERVICE_UUID)
        self.service_uuid_cell.value = service_uuid
        device_uuid = settings.get_device_uuid()
        print('Device UUID db gave me is', device_uuid)
        self.device_uuid_cell.value = device_uuid

    def on_pre_enter(self):
        self.load_settings()