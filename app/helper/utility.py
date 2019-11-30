import re
from flask import jsonify

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
