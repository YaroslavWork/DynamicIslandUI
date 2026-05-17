import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class BaseWidget(Gtk.Box):
    __gtype_name__ = 'BaseWidget'

    def __init__(self, config=None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}

    def update(self):
        """Update the widget state. Override in subclasses."""
        pass

    def destroy_widget(self):
        """Clean up timeouts and resources. Override in subclasses."""
        pass
