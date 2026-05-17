import sys
import os

os.environ["WGPU_GUI_BACKEND"] = "offscreen"
os.environ["RENDERCANVAS_BACKEND"] = "offscreen"

try:
    import gi

    gi.require_version('Gtk', '4.0')
    gi.require_version('Gtk4LayerShell', '1.0')
    
    from gi.repository import Gtk, Gtk4LayerShell
    print("Success: PyGObject, GTK4 and GTK4LayerShell are installed")

except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

except ValueError as e:
    print(f"Error: GTK integration is failed: {e}")
    sys.exit(1)


try:
    import wgpu
    import wgpu.backends.wgpu_native
    
    adapter = wgpu.gpu.request_adapter_sync()
    print(f"Success: WGPU is installed and GPU is {adapter.features}")

except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

except Exception as e:
    print(f"Error: WGPU integration is failed: {e}")
    sys.exit(1)

print("\n All dependencies are installed and configured.")