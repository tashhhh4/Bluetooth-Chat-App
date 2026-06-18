from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from db.manager import settings

class AppIDCell(BoxLayout):

    def __init__(self, **kwargs):
        super(AppIDCell, self).__init__(**kwargs)

        self.orientation='vertical'
        self.label = Label(text='Print results here')
        self.add_widget(self.label)

        self.run_settings_test()

    def run_settings_test(self):
        service_uuid = settings.get_service_uuid()
        print('SERVICE UUID:', service_uuid)
        self.label.text = f'SERVICE UUID: {service_uuid}'


class DebugSettings(GridLayout):

    def __init__(self, **kwargs):
        super(DebugSettings, self).__init__(**kwargs)

        self.cols=2
        self.spacing = 5
        self.padding = 5

        self.app_id_cell = AppIDCell()
        self.add_widget(self.app_id_cell)
