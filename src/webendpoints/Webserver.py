from flask import Flask, request, Response, send_from_directory, redirect
import Program
import ProgramInfo as ProgInfo
from multiprocessing import Process
import ProgramInfo as __ProgInfo
import os.path
import json

# The flash-rest-api
app = Flask("Poxelbox-Configuration-API")


##############
### Webapp ###
##############

# Returns the webserver directory
def webserver_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__)) + "/../rsc/webserver/Poxelbox-Configtool-Web/app"


# Serves the web-app for configuration
@app.route('/app/<path:filename>')
def access_webapp(filename):
    return send_from_directory(webserver_dir(), filename)


# Directly serves the index-html when only requesting the root
@app.route('/app/')
def webapp_quality_of_life():
    return send_from_directory(webserver_dir(), "index.html")


# Redirecty directly to the webapp
@app.route("/")
def root():
    return redirect("/app/")


#####################
### API Endpoints ###
#####################

# Required for browsers to accept cross-origin requests
@app.route("/api/push-view", methods=['OPTIONS'])
def __push_view_pre():
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'content-type'
    return resp


# Returns the fully exported configuration
@app.route('/api/get-view', methods=['GET'])
def __get_view():
    resp = Response(Program.config_loader.export_full_to_json())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Accepts updated settings data
@app.route("/api/push-view", methods=["POST"])
def __push_view():
    # Tries to load the config
    res = Program.config_loader.validate_and_extend_json_config(request.json)

    # Exports, writes and updates the file
    raw_json = json.dumps(request.json)

    # Checks for an invalid pass or invalidly long configs
    if res == False or len(raw_json) > 2000:
        resp = Response("Invalid request", 400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # Writes the new config
    with open(__ProgInfo.CONFIG_PATH, mode='w') as fp:
        fp.write(raw_json)

    resp = Response("Success", 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    Program.preload_stop()

    return resp


# Event: Runs once when the server is started inside a different thread (Process)
def __async_start():
    app.run(port=ProgInfo.WEB_PORT, host='0.0.0.0')


# Starts the webserver and return it's process
def start():
    p = Process(target=__async_start)
    p.start()
    return p
