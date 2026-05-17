# Installation Process for Archlinux (Wayland)


- Open the Terminal and run the following commands:
```bash
    sudo pacman -Syu
    sudo pacman -S python python-pip base-devel pkgconf \
               gobject-introspection gtk4 gtk4-layer-shell \
               cairo
```


- Create a virtual environment for the project:
```bash
    python -m venv .venv
    source .venv/bin/activate
```

- Install the python packages:
```bash
    pip install -r requirements.txt
```

- Run the test script to verify the installation:
```bash
    python test_setup.py
```

If all set and ready, run the main script:
```bash
    LD_PRELOAD=/usr/lib/libgtk4-layer-shell.so ./.venv/bin/python main.py
```