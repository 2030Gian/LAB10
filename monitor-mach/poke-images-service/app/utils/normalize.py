import re


def normalize_name(value: str) -> str:
    if value is None:
        return ""

    value = value.strip().lower()
    value = value.replace("♀", "f")
    value = value.replace("♂", "m")
    value = re.sub(r"[^a-z0-9]", "", value)

    return value