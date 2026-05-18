import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import threading

import os

class BaseWidget(Gtk.Box):
    __gtype_name__ = 'BaseWidget'

    def __init__(self, config=None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}
        
        # Automatically infer widget name and load its local.css
        module_name = self.__module__
        if module_name.startswith("widgets."):
            parts = module_name.split(".")
            if len(parts) >= 2:
                widget_name = parts[1]
                css_path = f"widgets/{widget_name}/local.css"
                if os.path.exists(css_path):
                    css_provider = Gtk.CssProvider()
                    css_provider.load_from_path(css_path)
                    self.get_style_context().add_provider(
                        css_provider,
                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                    )

    def update(self):
        """Update the widget state. Override in subclasses."""
        pass

    def destroy_widget(self):
        """Clean up timeouts and resources. Override in subclasses."""
        pass

    def run_in_background(self, task_func, callback_func=None, *args, **kwargs):
        """
        Run a task in a background thread and optionally call a callback 
        on the main thread with the result.
        
        :param task_func: Function to run in the background.
        :param callback_func: Function to call on the main thread with the result.
        """
        def worker():
            try:
                result = task_func(*args, **kwargs)
                if callback_func:
                    # GLib.idle_add ensures callback_func runs on the main GTK thread
                    GLib.idle_add(callback_func, result)
            except Exception as e:
                print(f"Background task failed: {e}")
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread
