class ConfigError(Exception):
    pass


def read_settings(path):
    ok = True
    error = ""
    try:
        f = open(path)
    except:
        ok = False
        error = "cannot open " + path
    if ok == False:
        raise ConfigError(error)

    settings = {}
    lines = f.readlines()
    n = 0
    for line in lines:
        n = n + 1
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if not "=" in line:
            f.close()
            raise ConfigError("line " + str(n) + ": expected key=value")
        parts = line.split("=", 1)
        key = parts[0].strip()
        value = parts[1].strip()
        is_int = True
        try:
            int(value)
        except:
            is_int = False
        if is_int == True:
            settings[key] = int(value)
        elif value.lower() == "true" or value.lower() == "yes":
            settings[key] = True
        elif value.lower() == "false" or value.lower() == "no":
            settings[key] = False
        else:
            settings[key] = value
    f.close()
    return settings
