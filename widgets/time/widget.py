import gi
import time
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class Widget(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_css_class("time-widget")
        self.add_css_class("widget")
        self.label = Gtk.Label()
        self.append(self.label)
        self.update_time()
        # Update time every second
        GLib.timeout_add_seconds(1, self.update_time)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.label.set_label(current_time)
        return True # Return True to keep the timeout active
