
message = {
    "a": "Error: Typos in instruction name or register name",
    "b": "Error: Use of undefined variables",
    "c": "Error: Use of undefined labels",
    "d": "Error: Illegal use of FLAGS register",
    "e": "Error: Illegal Immediate values (less than 0 or more than 255)",
    "f": "Error: Misuse of labels as variables or vice-versa",
    "g": "Error: Variables not declared at the beginning",
    "h": "Error: Missing hlt instruction.",
    "i": "Error: <hlt> not being used as the last instruction",
    "j": "Error: Wrong syntax used for instructions",
    "k": "General Syntax Error",
    "l": "Error: Multiple declaration of same label",
    "m": "Error: Multiple declaration of same variable",
    "n": "Error: Multiple declaration of <hlt> instruction",
}


def error_no_halt():
    print(message["h"])


def error_note(error, line):
    print(f"{message[error]} at line + {line}.")
