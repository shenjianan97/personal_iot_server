from flask import Flask, request
from yeelight import discover_bulbs, Bulb
import json

from yeelight.main import BulbException

app = Flask(__name__)

IP = 'ip'
BRIGHTNESS = 'brightness'
COLORTEMP = 'colortemp'

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
        return 'success'
    else:
        return 'bad request!', 400

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
            return str(e), 404
        return 'success'
    else:
        return 'bad request!', 400

@app.route('/setbrightness', methods=['POST'])
def setbrightness():
    content = request.json
    print(content)
    if IP in content and BRIGHTNESS in content and len(content) == 2:
        bulb = Bulb(content[IP])
        bulb.set_brightness(int(content[BRIGHTNESS]))
        return 'success'
    else:
        return 'bad request!', 400

@app.route('/setcolortemp', methods=['POST'])
def setcolortemp():
    content = request.json
    print(content)
    if IP in content and COLORTEMP in content and len(content) == 2:
        bulb = Bulb(content[IP])
        bulb.set_color_temp(int(content[COLORTEMP]))
        return 'success'
    else:
        return 'bad request!', 400


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5002)