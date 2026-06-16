from kivy.app import App
from kivy.properties import NumericProperty
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

# Helper functions
def pluralize(text, number):
    if number == 1:
        return text
    return text + 's'

class Counter(Label):

    counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Counter, self).__init__(**kwargs)
        self.update_text()

    def on_counter(self, instance_, value_):
        self.update_text()

    def update_text(self):
        times = pluralize('time', self.counter)
        self.text = f'The button has been pressed {self.counter} {times}.'

    def increment(self):
        self.counter += 1


class DebugMessages(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.counter = Counter()
        self.add_widget(self.counter)
        for msg in SAMPLE_MESSAGES:
            text = msg['text']
            sender = msg['from']
            when = msg['send_date']
            self.add_widget(Label(
                    text=f'\"{text}\" -- Sent by {sender} {when}',
                    text_size=[300, 100]
                ),
            )
        self.message_input = TextInput(multiline=True)
        self.add_widget(self.message_input)
        self.send_button = Button(text='Send Message')
        self.send_button.bind(on_press=self.push_button)
        self.add_widget(self.send_button)

    # Button Functions
    def push_button(self, button_instance):
        self.counter.increment()


class Blu2App(App):
    def build(self):
        return DebugMessages()
        # return Label(text='Simple Label')

Blu2App().run()