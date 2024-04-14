import json

from flask import Flask, redirect, session, request, json
from flask_cors import CORS, cross_origin
from server.auth.auth import authorize, oauth2callback
from server.customers.list_accessible_customers import list_accessible_customers
from server.ga_runner import REFRESH_ERROR

_CLIENT_URL = "http://localhost:4200"

app = Flask(__name__)
app.secret_key = "SECRET KEY"
cors = CORS(app, resources={r"/*": {"origins": _CLIENT_URL}})  # Corrected "ressources" to "resources"

@app.route("/authorize")
def authorize_endpoint():
    token = request.args.get("token")
    session["token"] = token
    auth_info = authorize()
    passthrough_val = auth_info["passthrough_val"]
    session["passthrough_val"] = passthrough_val
    url = auth_info["authorization_url"]
    return redirect(url)

@app.route("/oauth2callback")
def oauth2callback_endpoint():
    token = session["token"]
    passthrough_val = session["passthrough_val"]
    state = request.args.get("state")
    code = request.args.get("code")
    oauth2callback(passthrough_val, state, code, token)
    return redirect(_CLIENT_URL)

@app.route("/customers")
@cross_origin()
def customers():
    headers = request.headers
    token = headers["token"]
    try:
        resource_names = list_accessible_customers(token)  # Corrected variable name from ressource_names to resource_names
        return json.dumps(resource_names)  # Assuming list_accessible_customers returns a list of resource names
    except Exception as ex:
        return handleException(ex)

def handleException(ex):
    error = str(ex)  # Corrected variable name from errors to error
    if error == REFRESH_ERROR:  # Corrected variable name from errors to error
        return json.dumps({
            "code": 401,
            "name": "INVALID REFRESH TOKEN",
            "description": error
        })
    else:
        return json.dumps({
            "code": 500,
            "name": "INTERNAL_SERVER_ERROR",
            "description": error
        })

if __name__ == "__main__":
    app.run(debug=True)