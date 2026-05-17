# How to create a new widget

### To create a new widget folder:
```bash
    mkdir widgets/[widgetName]
    cd widgets/[widgetName]
    touch builder.xml local.css widget.py
```

### Inside widget.py you must to stick to this rule:
- The class name must be: Widget(BaseWidget) and you must import it: from widgets.base import BaseWidget.
- In the widget class, you must add a __init__ method and call super().__init__(**kwargs).
- In builder.xml you must define a <template class="Widget" parent="BaseWidget">
- You must to use @Gtk.Template(filename=os.path.join(os.path.dirname(__file__), 'builder.xml')).
- You must to use __gtype_name__ = '[widgetName]Widget'
- You can add some styling for the widget in local.css inside the widget folder.

### After creating the widget, you must to add it to the config.toml file:
```toml
[widgets.left]
names = ["widgetName"]

[widgets.right]
names = ["widgetName"]
```