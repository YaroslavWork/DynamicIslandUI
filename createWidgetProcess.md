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
- In config.toml file in [widgetName] table add all parameters of your widget.
- In builder.xml you must define a <template class="Widget" parent="BaseWidget">
- You must to use @Gtk.Template(filename=os.path.join(os.path.dirname(__file__), 'builder.xml')).
- You must to use __gtype_name__ = '[widgetName]Widget'
- You can add some styling for the widget in local.css inside the widget folder.
- To run heavy tasks without freezing the UI, use `self.run_in_background(task_func, callback_func)`.

### After creating the widget, you must to add it to the config.toml file:
```toml
[widgets.left]
names = ["widgetName"]

[widgets.right]
names = ["widgetName"]
```

## To communicate with Dynamic Island:

We use the global `EventBus` to emit signals. All payloads should be dictionaries.

**Core Signals:**
- `island:resize` - `{"name": "widgetName", "width": 200, "height": 50}`
  *(Requests the main island to resize to accommodate this widget)*
- `island:connect` - `{"name": "widgetName"}`
  *(Announces the widget is ready)*
- `island:disconnect` - `{"name": "widgetName"}`
  *(Closes or hides the widget)*
- `island:duration` - `{"name": "widgetName", "duration_ms": 3000}`
  *(Sets how long the widget should stay visible; -1 for infinite)*

**Data & Context Signals:**
bus.emit("island:build_widget", {
    "name": "widgetName",
    "xml": """
        <interface>
            <object class="GtkBox" id="root_box">
                <property name="orientation">horizontal</property>
                <property name="spacing">10</property>
                <child>
                    <object class="GtkImage" id="icon"/>
                </child>
                <child>
                    <object class="GtkLabel" id="title"/>
                </child>
            </object>
        </interface>
    """,
    "css": "#root_box { background-color: black; border-radius: 20px; padding: 10px; }"
})
- `island:update_context` - `{"name": "widgetName", "data": {"title": "...", "value": 100}}`
  *(Passes dynamic runtime data to a widget so it can update its GTK UI elements)*