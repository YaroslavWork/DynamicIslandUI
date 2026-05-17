import sys
import os
from datetime import datetime

from settings import config

os.environ["WGPU_GUI_BACKEND"] = "offscreen"
os.environ["RENDERCANVAS_BACKEND"] = "offscreen"

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Gtk4LayerShell, GLib, Gdk

class MainTaskbar(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        edge = Gtk4LayerShell.Edge.BOTTOM if config["general"]["anchor"] == "bottom" else Gtk4LayerShell.Edge.TOP
        margin_edge = config["general"]["margin_edge"]
        margin_side_edge = config["general"]["margin_side_edge"]

        Gtk4LayerShell.init_for_window(self)

        # Set the layer to display above normal windows
        Gtk4LayerShell.set_layer(self, Gtk4LayerShell.Layer.TOP)

        # Enable auto exclusive zone to reserve space and shrink other windows
        Gtk4LayerShell.auto_exclusive_zone_enable(self)

        # Anchor to the configured edge (TOP or BOTTOM)
        Gtk4LayerShell.set_anchor(self, edge, True)
        
        # Anchor LEFT and RIGHT to make it span across the screen like a taskbar
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.LEFT, True)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.RIGHT, True)

        # Set margins
        Gtk4LayerShell.set_margin(self, edge, margin_edge)
        Gtk4LayerShell.set_margin(self, Gtk4LayerShell.Edge.LEFT, margin_side_edge)
        Gtk4LayerShell.set_margin(self, Gtk4LayerShell.Edge.RIGHT, margin_side_edge)

        self.set_title("Dynamic Island UI")
        
        # Set height from config
        height = config.get("widget_default", {}).get("height", 40)
        self.set_default_size(0, height)

def on_activate(app):
    win = MainTaskbar(application=app)
    win.present()

if __name__ == "__main__":
    app = Gtk.Application(application_id="org.dynamic_island.ui")
    app.connect("activate", on_activate)
    app.run(sys.argv)