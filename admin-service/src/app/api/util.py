def cast_value(value):
    if not value:
        raise Exception("Error, need value present")
    try:
        value = int(value)
    except Exception:
        pass
    if value == 'true' or value == 'True' or value == 'False' or value == 'false' or isinstance(value, bool):
        if not isinstance(value, bool):
            value = True if value == 'true' or value == 'True' else False
    else:
        if not isinstance(value, int):
            value = str(value)
    return value
