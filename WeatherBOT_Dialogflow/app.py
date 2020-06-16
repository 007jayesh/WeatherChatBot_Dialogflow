 #Step0
'''importing all the required directories'''

from flask import Flask, request, make_response
import json
import pyowm
import os
from flask_cors import CORS,cross_origin


#Step1
app = Flask(__name__)


#Step2
'''Providing weather api key '''

#owmapikey= os.environ.get('d298fbe5ba6352a8a6f2b766ecef2d72')
owmapikey = '49e2df7968956eff764af3ffad2245c9'
owm = pyowm.OWM(owmapikey)


#Step3
'''Code for receiving and forwarding responses to google dialogflow'''

@app.route('/webhook', methods = ['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Request:')
    print(json.dumps(req))

    res = processRequest(req)

    res = json.dumps(res)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#Step4
'''Processing requests from dialogflow'''

def processRequest(req):
    result = req.get('queryResult')
    parameters = result.get('parameters')
    city = parameters.get('cityName')
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat = str(latlon_res.get_lat())
    lon = str(latlon_res.get_lon())

    wind_res = w.get_wind()
    wind_speed = str(wind_res.get('speed'))

    humidity = str(w.get_humidity())

    celsius_result = w.get_temperature('celsius')
    temp_min_celsius =str(celsius_result.get('temp_min'))
    temp_max_celsius =str(celsius_result.get('temp_max'))

    fahrenheit_result = w.get_temperature('fahrenheit')
    temp_min_fahrenheit = str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit = str(fahrenheit_result.get('temp_max'))
    speech = 'Today the weather in ' + city + ': \n'+ 'Humidity :' + humidity + '.\n Wind Speed :' + wind_speed

    return {
        'fulfillmentText': speech,
        "displayText": speech
    }


#Step5
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app on port %d' % port)
    app.run(debug=False, port=port)








