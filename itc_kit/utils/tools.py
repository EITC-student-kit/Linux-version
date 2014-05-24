__author__ = 'Kristo Koert'

import threading
from itc_kit.settings import settings


def play_notification_sound():
    from os import system
    system("aplay ~/.itc-kit/notif_sound.wav")


class UrlChecker(threading.Thread):
    """
    This class performs a check to see whether the supplied url is valid or not.

    The check is minimalistic, a way this could be bypassed, is if the url is a text file somewhere that is downloaded
    and contains the string BEGIN:VCALENDAR.

    No check if this is not a valic ical file. (Anything besides the ical files of IT college.)
    """
    def __init__(self, instance):
        """
        :type instance: SetIcalUrlWindow
        """
        threading.Thread.__init__(self)
        self.instance = instance

    def run(self):
        self.instance._is_checking_url = True
        url = self.instance.entry.get_text()
        try:
            is_valid_ical_url(url)
            settings.update_settings("Timetable", "user_url", url)
            self.instance.info_label = "URL Verified and saved!"
        except Exception:
            self.instance.info_label = "Unable to verify, or invalid URL."
        self.instance._is_checking_url = False


def is_valid_ical_url(url):
    download_ical(url)


def download_ical(url):
    """Returns ical text from url.
    :rtype: str
    """
    import urllib.request
    req = urllib.request.urlopen(url)
    text = req.read().decode(encoding='UTF-8')
    if "BEGIN:VCALENDAR" not in text:
        raise ValueError
    return text


def string_from_till(a_string, first_symbol, second_symbol):
    """Returns the part of the string till next occurrence of symbol, if not present, returns whole string."""
    a_string = a_string[a_string.find(first_symbol):]
    indx = 0
    while indx + len(second_symbol) < len(a_string):
        if a_string[indx:indx + len(second_symbol)] == second_symbol:
            return a_string[:indx]
        else:
            indx += 1
    return a_string


def is_valid_hex(val):
    """
    :rtype bool
    """
    try:
        int(val, 16)
        return True
    except ValueError:
        return False
