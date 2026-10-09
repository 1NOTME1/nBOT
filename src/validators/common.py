def validate_positive_int(value):
    if type(value) is not int or value < 1:
        raise ValueError("Invalid value")
    return value

def validate_non_empty_string(value):
    if not isinstance(value, str) or value.strip() == "":
        raise ValueError("Invalid value")
    return value.strip()

def validate_positive_number(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError("Invalid value")
    return value

def validate_non_negative_int(value):
    if type(value) is not int or value < 0:
        raise ValueError("Invalid value")
    return value