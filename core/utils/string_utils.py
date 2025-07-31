import re

def pascal_to_snake(s: str) -> str:
    """
    Convert PascalCase to snake_case
    :param s: original PascalCase string
    :return: converted snake_case string
    """
    new = s[0].lower()
    for c in s[1:]:
        if c.isupper():
            new += f"_{c.lower()}"
        else:
            new += c
    return new

def snake_to_pascal(s: str) -> str:
    """
    Convert snake_case to PascalCase
    :param s: original snake_case string
    :return: converted PascalCase string
    """
    new = re.sub(r'(?:^|_)(\w)', lambda m: m.group(1).upper(), s)
    # m.group(1) -> get group idx 1
    #(where 0 is the first bracket which is non-capturing group
    return new


