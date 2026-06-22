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


def repr_advertisement(advertisement):
    """ Prints out the details of an Advertisement (able library) from a BLE device scan. """
    output = ''
    for ad in advertisement.parse(advertisement.data):
        output += f'TYPE: {ad.ad_type}; LEN: {len(ad.data)}; DATA: {ad.data.hex()}\n'
    return output
