from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def fit_height(widget):
    """ Sets a widget to grow its height according to its children. """
    widget.bind(minimum_height=widget.setter('height'))

def wrap_text(widget):
    """ Wraps text in the given widget.
        Only works if the widget has a fixed width.
    """
    widget.bind(
        size=lambda ins, _: setattr(
            ins, 'text_size', (ins.width, None)
        )
    )

def add_background(widget, color):
    """ Adds a color background to 'widget'. Expects a 4-value tuple for the color. """
    with widget.canvas.before:
        Color(*color)
        widget.bg_rect = Rectangle(pos=widget.pos, size=widget.size)

    def update(w, *args):
        w.bg_rect.pos = w.pos
        w.bg_rect.size = w.size

    widget.bind(pos=update, size=update)

def add_rows(parent_widget, data, height=50, col_widths=None, actions=None):
    """ Adds a child row with multiple columns, setting a consistent width for each field.
        'data' must be a list of values that have a __str__ method.
        if 'col_widths' is not None, it must be equal in length to 'data'.
    """
    if col_widths is not None:
        if data:
            expected_num_fields = len(data[0])
            if actions:
                expected_num_fields += len(actions[0].keys())
            if not len(col_widths) == expected_num_fields:
                raise TypeError('Expected', expected_num_fields, 'col_widths.')

    if actions is not None:
        if data:
            num_rows = len(data)
            if not len(actions) == num_rows:
                raise TypeError('Expected', num_rows, 'action functions.')

    for row, item in enumerate(data):
        row_widget = BoxLayout(size_hint_y=None, height=height)
        parent_widget.add_widget(row_widget)
        for col, value in enumerate(item):
            cell_widget = Label(
                text=str(value),
                height=height,
                size_hint_y=None,
                halign='left',
                valign='middle',
                width=col_widths[col] if col_widths else 200,
            )
            wrap_text(cell_widget)
            row_widget.add_widget(cell_widget)
        if actions:
            action_dict = actions[row]
            for key in action_dict:
                action_button = Button(text=key)
                action_button.bind(on_press=action_dict[key])
                row_widget.add_widget(action_button)
