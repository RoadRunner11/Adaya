from app import app
import json

@app.after_request
def jsonify_response(response):
    json_response = json.loads(response.get_data())
    response.set_data(json.dumps(json_response))
    return response