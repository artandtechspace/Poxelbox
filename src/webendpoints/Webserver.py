from flask import Flask, jsonify, request
import Program
import ProgramInfo as ProgInfo
from multiprocessing import Process
import ProgramInfo as __ProgInfo

# The flash-rest-api
app = Flask(__name__)


# Returns the fully exported configuration
@app.route('/get-view', methods=['GET'])
def __get_view():
    return Program.config_loader.export_full_to_json()


@app.route("/push-view", methods=["POST"])
def __push_view():
    # Tries to load the config
    res = Program.config_loader.try_load_from_json(request.json)

    if res == False:
        return "Invalid request", 400

    with open(__ProgInfo.CONFIG_PATH, mode='w') as fp:
        # Exports, writes and updates the file
        fp.write(Program.config_loader.export_to_json())

    return "", 200

# Event: Runs once when the server is started inside a different thread (Process)
def __async_start():
    app.run(port=ProgInfo.WEB_PORT)


# Starts the webserver and return it's process
def start():
    p = Process(target=__async_start)
    p.start()
    return p
