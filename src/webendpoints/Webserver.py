from flask import Flask, request, Response
import Program
import ProgramInfo as ProgInfo
from multiprocessing import Process
import ProgramInfo as __ProgInfo

# The flash-rest-api
app = Flask("Poxelbox-Configuration-API")


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


@app.route("/api/push-view", methods=["POST"])
def __push_view():
    # Tries to load the config
    res = Program.config_loader.try_load_from_json(request.json)

    if res == False:
        resp = Response("Invalid request", 400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    with open(__ProgInfo.CONFIG_PATH, mode='w') as fp:
        # Exports, writes and updates the file
        fp.write(Program.config_loader.export_to_json())

    resp = Response("Success", 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    Program.stop()

    return resp


# Event: Runs once when the server is started inside a different thread (Process)
def __async_start():
    app.run(port=ProgInfo.WEB_PORT, host='0.0.0.0')


# Starts the webserver and return it's process
def start():
    p = Process(target=__async_start)
    p.start()
    return p
