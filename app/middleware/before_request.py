
from app import app


@app.before_request
def before_request(response):
    """
    before_request contains actions before request
    
    Args:
        response ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    return response