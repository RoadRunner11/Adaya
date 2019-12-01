import re
from flask import jsonify, has_request_context

def res(body='OK', error='', status=200):
    """
    res is the default response object

    Args:
        body (any): main data return back to client
        status (int, optional): Defaults to 200.
        error (str, optional):  Defaults to ''.

    Returns:
        (json string, int): response object to client
    """
    return jsonify(body=body, error=error), status

def parse_int(chars):
    """
    parse_int converts string number to integer
    
    Args:
        chars (string):
    
    Returns:
        int: default to None
    """
    if chars:
        return int(chars) if chars.isdigit() else None
    return None