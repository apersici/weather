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


if __name__ == '__main__':

    app.run(debug=True, port=int(environ.get('PORT', 5000)))