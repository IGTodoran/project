"""Hello World app from Udacity Cloud course."""
import logging

from flask import json, Flask

app = Flask(__name__)


@app.route("/")
def hello():
    """Basic Hello World! message"""
    # Logging a CUSTOM message 
    app.logger.debug('Main request successfull')
    return "Hello World!"


@app.route('/status')
def status():
    """Endpoint returning the status of the app."""
    response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug("Status successfully returned.")
    return response


@app.route('/metrics')
def metrics():
    """Endpoint returning some useful metrics of the app."""
    response = app.response_class(
            response=json.dumps({"status": "success", "code": 0, "data": {"UserCount": 140, "UserCountActive": 23}}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info("Metrics successfully returned.")
    return response


if __name__ == "__main__":
    # Stream logs to a file, and set the default log level to DEBUG
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    app.run(host='0.0.0.0')
