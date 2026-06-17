from kivy.clock import Clock

def pluralize(text, number):
    if number == 1:
        return text
    return text + 's'

def schedule(func):
    """ Wrapper for Kivy.clock.Clock.schedule_once, because
        I find the name confusing.
    """
    Clock.schedule_once(func)