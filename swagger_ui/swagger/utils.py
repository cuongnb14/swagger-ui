def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # d.iteritems isn't used as you can't del or the iterator breaks.
    result = d.copy()
    for key, value in d.items():
        if value is None or value == "":
            del result[key]
        elif isinstance(value, dict):
            result[key] = del_none(value)
    return result
