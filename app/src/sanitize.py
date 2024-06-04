from flask import jsonify, Response
import re


def is_integer(value: str) -> bool:
    return (re.fullmatch(r"-?\d+", value) is not None)


def is_dangerous(value: str) -> bool:
    unsafe_pattern = r"[\'\";\\/<>()|=+\-\[\]]"
    return bool(re.search(unsafe_pattern, value))


def sanitize(args: list[tuple[str, type]]) -> (bool, Response, int):
    """
    Checks if parameters provided in query are of desired format.
    Every parameter desired as integer should contain only digits.
    Every parameter desired as string is checked for dangerous characters.
    If any parameter doesn't meet expectations function won't execute and will return http 400 code.
    :param args: List of tuples containing parameter and it's desired type.
    """
    for arg in args:
        # Optional arguments may be passed as None, this condition prevents it from being passed to regex.
        if not arg[0]:
            continue
        elif arg[1] == int:
            if not is_integer(arg[0]):
                return False, jsonify({"status": "fail", "message": "incorrect_parameter_format", "parameter": arg[0]}), 400
        elif arg[1] == str:
            if is_dangerous(arg[0]):
                return False, jsonify({"status": "fail", "message": "forbidden_characters_used", "parameter": arg[0]}), 400
    return True, jsonify({"status": "success"}), 200
