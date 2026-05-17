import sys
import os
from datetime import datetime
import importlib

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

        self.center_box = Gtk.CenterBox()
        self.set_child(self.center_box)

        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box.set_start_widget(self.left_box)

        self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box.set_end_widget(self.right_box)

        self.load_widgets()

    def load_widgets(self):
        left_widgets = config.get("widgets", {}).get("left", {}).get("names", [])
        right_widgets = config.get("widgets", {}).get("right", {}).get("names", [])

        for widget in left_widgets:
            try:
                module_path = f"widgets.{widget}.widget"
                module = importlib.import_module(module_path)
                if hasattr(module, "Widget"):
                    self.left_box.append(module.Widget())
            except Exception as e:
                print(f"Failed to load widget {widget}: {e}")

        for widget in right_widgets:
            try:
                module_path = f"widgets.{widget}.widget"
                module = importlib.import_module(module_path)
                if hasattr(module, "Widget"):
                    self.right_box.append(module.Widget())
            except Exception as e:
                print(f"Failed to load widget {widget}: {e}")

def load_css():
    css_provider = Gtk.CssProvider()
    try:
        css_provider.load_from_path('main.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    except Exception as e:
        print(f"Failed to load main.css: {e}")
        
    # Connect all the local.css files
    for widget in config["widgets"]["left"]["names"] + config["widgets"]["right"]["names"]:
        try:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(f"widgets/{widget}/local.css")
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception as e:
            print(f"Failed to load local.css: {e}")

    # Load dynamic CSS from config
    try:
        border_radius = config.get("widget_default", {}).get("border_radius", 12)
        dynamic_css = f".widget {{ border-radius: {border_radius}px; }}"
        dynamic_provider = Gtk.CssProvider()
        try:
            dynamic_provider.load_from_string(dynamic_css)
        except AttributeError:
            dynamic_provider.load_from_data(dynamic_css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            dynamic_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    except Exception as e:
        print(f"Failed to load dynamic CSS: {e}")

def on_activate(app):
    load_css()
    win = MainTaskbar(application=app)
    win.present()

if __name__ == "__main__":
    app = Gtk.Application(application_id="org.dynamic_island.ui")
    app.connect("activate", on_activate)
    app.run(sys.argv)