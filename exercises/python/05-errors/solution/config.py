TRUE_WORDS = ("true", "yes")
FALSE_WORDS = ("false", "no")


class ConfigError(Exception):
    pass


def parse_value(text):
    """Turn a raw config value into an int, a bool, or leave it as a string."""
    try:
        return int(text)
    except ValueError:
        pass
    if text.lower() in TRUE_WORDS:
        return True
    if text.lower() in FALSE_WORDS:
        return False
    return text


def read_settings(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError as err:
        raise ConfigError("cannot open " + path) from err

    settings = {}
    for line_number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"line {line_number}: expected key=value")
        key, value = line.split("=", 1)
        settings[key.strip()] = parse_value(value.strip())
    return settings
