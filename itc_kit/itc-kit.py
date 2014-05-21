#!/usr/bin/python3

__author__ = 'Kristo Koert'

from itc_kit.gui import toolbarindicator
from itc_kit.mail import email_system
from itc_kit.core import notification_system
from gi.repository import Gtk, Gdk
from itc_kit.conky.conky import Conky

if __name__ == "__main__":

    Gdk.threads_init()
    indicator = toolbarindicator.activate_toolbar()

    Gdk.threads_leave()
    conky_thread = Conky()
    conky_thread.start()
    Gdk.threads_enter()

    Gdk.threads_leave()
    email_thread = email_system.MailHandler()
    email_thread.start()
    Gdk.threads_enter()

    Gdk.threads_leave()
    notification_thread = notification_system.NotificationHandler(indicator, indicator.main_menu)
    notification_thread.start()
    Gdk.threads_enter()

    Gtk.main()
