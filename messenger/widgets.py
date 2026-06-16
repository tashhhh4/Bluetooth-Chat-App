from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from db.manager import messages

class DebugMessages(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        # Scrollable Message Container
        self.messages = messages.get_all()
        self.scroll = ScrollView()
        self.message_container = GridLayout(
            cols=1,
            spacing=4,
            size_hint_y=None,
        )
        self.message_container.bind(
            minimum_height=self.message_container.setter('height')
        )

        self.scroll.add_widget(self.message_container)
        self.add_widget(self.scroll)

        for msg in self.messages:
            self.add_message_widget(msg)

        # Bottom Text Input
        input_bar = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=140,
            spacing=5,
        )
        self.message_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=90
        )
        self.send_button = Button(
            text='Send Message',
            size_hint_y=None,
            height=40,
        )
        self.send_button.bind(on_press=self.push_button)

        input_bar.add_widget(self.message_input)
        input_bar.add_widget(self.send_button)
        self.add_widget(input_bar)

    def add_message_widget(self, msg):
        text = msg.text
        sender = msg.sender

        label = Label(
            text=f'"{text}"\n— {sender}',
            size_hint_y=None,
            halign='left',
            valign='middle',
            text_size=(280, None)
        )
        label.bind(
            texture_size=lambda inst, size: setattr(inst, 'height', size[1] + 10)
        )

        self.message_container.add_widget(label)

    def push_button(self, button_instance):
        text = self.message_input.text.strip()

        if not text:
            return

        messages.add_new(text)
