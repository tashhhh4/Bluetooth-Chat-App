from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

def add_background(widget, color):
    """ Adds a color background to 'widget'. Expects a 4-value tuple for the color. """
    with widget.canvas.before:
        Color(*color)
        widget.bg_rect = Rectangle(pos=widget.pos, size=widget.size)

    def update(w, *args):
        w.bg_rect.pos = w.pos
        w.bg_rect.size = w.size

    widget.bind(pos=update, size=update)

def add_rows(parent_widget, data, height=50, col_widths=None):
    """ Adds a child row with multiple columns, setting a consistent width for each field.
        'data' must be a list of values that have a __str__ method.
        if 'col_widths' is not None, it must be equal in length to 'data'.
    """
    if col_widths is not None:
        if data:
            num_fields = len(data[0])
            if not len(col_widths) == num_fields:
                raise TypeError('Expected', num_fields, 'col_widths.')

    for item in data:
        row_widget = BoxLayout()
        parent_widget.add_widget(row_widget)
        for col, value in enumerate(item):
            kwargs = {}
            if col_widths:
                kwargs['width'] = col_widths[col]
                kwargs['size_hint_x'] = None
            cell_widget = Label(text=value, height=height, **kwargs)
            row_widget.add_widget(cell_widget)