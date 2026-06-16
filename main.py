from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

SAMPLE_MESSAGES = [
    {
        'text': 'I\'m sitting in 45a. Wanna trade seats? I can offer you some peanuts.',
        'from': 'Galaxy 500SE',
        'send_date': '14 minutes ago'
    },
    {
        'text': 'Hi, how are you?',
        'from': 'Joe',
        'send_date': '5 seconds ago',
    },
    {
        'text': 'Can you come to my seat, honey? The baby is getting hungry.',
        'from': 'Husband',
        'send_date': 'Just now',
    },
]


class DebugMessages(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)
        self.orientation = 'vertical'
        for msg in SAMPLE_MESSAGES:
            text = msg['text']
            sender = msg['from']
            when = msg['send_date']
            self.add_widget(Label(text=f'\"{text}\" -- Sent by {sender} {when}'))
        self.message_input = TextInput(multiline=True)
        self.add_widget(self.message_input)
        self.add_widget(Button(text='Send Message'))


class Blu2App(App):
    def build(self):
        return DebugMessages()

Blu2App().run()