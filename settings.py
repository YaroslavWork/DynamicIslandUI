import sys
import tomllib

config = {}

try:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError:
    print("Error: config.toml not found")
    sys.exit(1)
except tomllib.TOMLDecodeError as e:
    print(f"Syntax error in config.toml: {e}")
    sys.exit(1)
