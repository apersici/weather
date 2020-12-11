from os import environ
import requests
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)


@app.route('/temp/<city>')
def temperature(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return make_response(f'Error getting temperature for {city.title()}!', 404)

    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        return jsonify(current_temperature)
    else:
        return f'Error getting temperature for {city.title()}'


@app.route('/pressure/<city>')
def pressure(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return make_response(f'Error getting pressure for {city.title()}!', 404)

    press = response.get('main', {}).get('pressure')
    if press:
        return jsonify(press)
    else:
        return f'Error getting pressure for {city.title()}'


@app.route('/humidity/<city>')
def humidity(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return make_response(f'Error getting humidity for {city.title()}!', 404)

    humidity = response.get('main', {}).get('humidity')
    if humidity:
        return jsonify(humidity)
    else:
        return f'Error getting humidity for {city.title()}'


@app.route('/wind/speed/<city>')
def wind(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return make_response(f'Error getting wind speed for {city.title()}!', 404)

    windspeed = response.get('wind', {}).get('speed')
    if windspeed:
        return jsonify(windspeed)
    else:
        return f'Error getting wind speed for {city.title()}'


@app.route('/aqi/<city>')
def aqi(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    google_key = environ.get('GOOGLE_KEY')
    googleUrl = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_key}'
    googleResponse = requests.get(googleUrl).json()

    result = googleResponse['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']

    latitude = geodata['lat']
    longitude = geodata['lng']

    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(url).json()

    airquality = response.get('list')[0].get('main', {}).get('aqi')
    if airquality:
        return jsonify(airquality)
    else:
        return f'Error getting air quality for city: {city.title()}'


if __name__ == '__main__':

    app.run(debug=True, port=int(environ.get('PORT', 5000)))