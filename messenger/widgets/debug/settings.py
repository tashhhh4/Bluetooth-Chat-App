from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import config
from db.manager import settings

class ServiceIDCell(BoxLayout):

    def __init__(self, **kwargs):
        super(ServiceIDCell, self).__init__(**kwargs)

        self.label = Label(text='Print results here')
        self.label.bind(width=lambda ins, val: setattr(ins, 'text_size', (val, None)))
        self.add_widget(self.label)

        self.run_settings_test()

    def run_settings_test(self):
        service_uuid = config.SERVICE_UUID
        print('SERVICE UUID:', service_uuid)
        self.label.text = f'SERVICE UUID: {service_uuid}'


class DeviceIDCell(BoxLayout):

    def __init__(self, **kwargs):
        super(DeviceIDCell, self).__init__(**kwargs)

        self.label = Label(text='Print results here')
        self.label.bind(width=lambda ins, val: setattr(ins, 'text_size', (val, None)))
        self.add_widget(self.label)

        self.run_get_device_id()

    def run_get_device_id(self):
        device_id = settings.get_device_uuid()
        self.label.text = f'DEVICE_UUID: {device_id}'


class SettingsList(BoxLayout):
    """ Show all the Settings that exist and allow deleting them for testing purposes. """

    DELETABLE = ['SERVICE_UUID', 'DEVICE_UUID']

    def __init__(self, **kwargs):
        super(SettingsList, self).__init__(**kwargs)

        self.orientation='vertical'

        self.table = GridLayout(
            cols=3,
            size_hint_y=None,
            row_default_height=160,
            row_force_default=True,
            spacing=5,
            padding=5,
        )
        self.table.bind(minimum_height=self.table.setter('height'))
        self.add_widget(self.table)

        self.add_header()
        self.add_rows()

    def add_header(self):
        for heading in ['KEY', 'VALUE', 'OPTIONS']:
            self.table.add_widget(Label(text=f'[b]{heading}[/b]', markup=True))

    def add_rows(self):
        app_settings = settings.list_all()

        for setting in app_settings:
            key_label = Label(
                text=setting.key,
                halign='left',
                valign='middle',
            )
            value_label = Label(
                text=setting.value,
                halign='left',
                valign='middle',
            )
            key_label.bind(width=lambda ins, val: setattr(ins, 'text_size', (val, None)))
            value_label.bind(width=lambda ins, val: setattr(ins, 'text_size', (val, None)))
            if setting.key in self.DELETABLE:
                key = setting.key
                def delete(_, key=key):
                    settings.delete(key)
                    self.table.clear_widgets()
                    self.add_header()
                    self.add_rows()
                delete_button = Button(text='Delete')
                delete_button.bind(on_press=delete)
            else:
                delete_button = Label(text='-')

            self.table.add_widget(key_label)
            self.table.add_widget(value_label)
            self.table.add_widget(delete_button)


class DebugSettings(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugSettings, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        settings_list = SettingsList()
        settings_list.size_hint_y = 0.3
        self.add_widget(settings_list)

        self.row_1 = BoxLayout(spacing=5, padding=5, height=200)
        self.add_widget(self.row_1)
        self.row_1.add_widget(ServiceIDCell(size_hint_x=0.5))
        self.row_1.add_widget(DeviceIDCell(size_hint_x=0.5))
