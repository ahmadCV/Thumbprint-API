import json
import time

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from fingerprint_nadra import get_fingerprint_video, base_64_encode

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route("/test", methods=['GET'])
def helloworld():
    return jsonify({"status": "200 OK"})


@app.route('/api/post/video', methods=['POST'])
def getVideo():
    if request.headers['Content-Type'] == 'application/json':
        time.sleep(1)
        data = request.json
        dims = data['dims']

        finger_1, finger_2 = get_fingerprint_video("output.mp4", dims)
        result = dict()
        finger_1 = base_64_encode(finger_1)
        finger_2 = base_64_encode(finger_2)
        result.update({"finger_1": finger_1, "finger_2": finger_2})

        return json.dumps(result)

    if request.headers['Content-Type'] == 'application/octet-stream':
        with open("output.mp4", "wb") as out_file:  # open for [w]riting as [b]inary
            out_file.write(request.data)

        print('Data written in txt file')

    return jsonify({'recieved_status': '200 OK'})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
