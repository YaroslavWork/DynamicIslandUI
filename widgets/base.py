import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import threading

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
