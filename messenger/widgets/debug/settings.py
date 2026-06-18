from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from db.manager import settings

class ServiceIDCell(BoxLayout):

    def __init__(self, **kwargs):
        super(ServiceIDCell, self).__init__(**kwargs)

        self.orientation='vertical'
        self.label = Label(text='Print results here')
        self.add_widget(self.label)

        self.run_settings_test()

    def run_settings_test(self):
        service_uuid = settings.get_service_uuid()
        print('SERVICE UUID:', service_uuid)
        self.label.text = f'SERVICE UUID: {service_uuid}'


class SettingsList(BoxLayout):
    """ Show all the Settings that exist and allow deleting them for testing purposes. """

    DELETABLE = ['TEST_SETTING']

    def __init__(self, **kwargs):
        super(SettingsList, self).__init__(**kwargs)

        self.orientation='vertical'

        self.table = GridLayout(
            cols=3,
            size_hint_y=None,
            row_default_height=80,
            row_force_default=True,
            spacing=5,
            padding=5,
        )
        self.table.bind(minimum_height=self.table.setter('height'))

        # Header row
        for heading in ['KEY', 'VALUE', 'OPTIONS']:
            self.table.add_widget(Label(text=f'[b]{heading}[/b]', markup=True))
        self.add_rows()
        self.add_widget(self.table)

    def add_rows(self):
        app_settings = [
            {'key': 'TEST_SETTING', 'value': 'example_value_123'},
            {'key': 'OTHER_SETTING', 'value': 'password123'},
        ]
        for setting in app_settings:
            if setting['key'] in self.DELETABLE:
                delete_button = Button(text='Delete')
            else:
                delete_button = Label(text='-')
            self.table.add_widget(Label(text=setting['key']))
            self.table.add_widget(Label(text=setting['value']))
            self.table.add_widget(delete_button)


class DebugSettings(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugSettings, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        self.add_widget(SettingsList())
        self.grid = GridLayout(cols=2, spacing=5, padding=5)
        self.add_widget(self.grid)
        self.grid.add_widget(ServiceIDCell())