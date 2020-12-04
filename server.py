from flask import Flask, request
from yeelight import discover_bulbs, Bulb
import json

from yeelight.main import BulbException

app = Flask(__name__)

IP = 'ip'
BRIGHTNESS = 'brightness'
COLORTEMP = 'colortemp'

SUCCESS_RESPONSE = {
    "status": "success"
}

ERROR_RESPONSE = {
    "status": "fail"
}

@app.route('/discover', methods=['GET'])
def discover():
    result = discover_bulbs()
    print(result)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/turnon', methods=['POST'])
def turnon():
    content = request.json
    print(content)
    if IP in content and len(content) == 1:
        bulb = Bulb(content[IP])
        try:
            bulb.turn_on()
        except BulbException as e:
            print(e)
            return str(e), 400
        return SUCCESS_RESPONSE
    else:
        return ERROR_RESPONSE, 400

@app.route('/turnoff', methods=['POST'])
def turnoff():
    content = request.json
    print(content)
    if IP in content and len(content) == 1:
        bulb = Bulb(content[IP])
        try:
            bulb.turn_off()
        except BulbException as e:
            print(e)
            return ERROR_RESPONSE
        return SUCCESS_RESPONSE
    else:
        return ERROR_RESPONSE, 400

@app.route('/setbrightness', methods=['POST'])
def setbrightness():
    content = request.json
    print(content)
    if IP in content and BRIGHTNESS in content and len(content) == 2:
        bulb = Bulb(content[IP])
        bulb.set_brightness(int(content[BRIGHTNESS]))
        return SUCCESS_RESPONSE
    else:
        return ERROR_RESPONSE, 400

@app.route('/setcolortemp', methods=['POST'])
def setcolortemp():
    content = request.json
    print(content)
    if IP in content and COLORTEMP in content and len(content) == 2:
        bulb = Bulb(content[IP])
        bulb.set_color_temp(int(content[COLORTEMP]))
        return SUCCESS_RESPONSE
    else:
        return ERROR_RESPONSE, 400


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5002)