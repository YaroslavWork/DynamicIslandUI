import gi
import time
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

import os

@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), 'builder.xml'))
class Widget(Gtk.Box):
    __gtype_name__ = 'TimeWidget'

    time_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_time()
        # Update time every second
        GLib.timeout_add_seconds(1, self.update_time)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.set_label(current_time)
        return True # Return True to keep the timeout active
