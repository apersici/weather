from os import environ
import requests
import telebot
from flask import Flask, render_template, request, jsonify, make_response
from telebot import *

app = Flask(__name__)


bot_token = environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode=None)

telegramUrl = f'https://api.telegram.org/bot{bot_token}'


def sendMessage(chat_id, text):
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    api_key = environ.get('API_KEY')
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r.get('message').get('chat').get('id')
        message = r.get('message').get('text')

        if message == '/start':
            sendMessage(chat_id, text=f'Welcome to WeatherBot! \nPlease input a city:')
        elif message == '/info':
            sendMessage(chat_id, text=f'You can get information about:\n'
                                      f'1) Temperature\n'
                                      f'2) Pressure\n'
                                      f'3) Humidity\n'
                                      f'4) Felt Temperature\n'
                                      f'5) Wind Speed\n'
                                      f'6) Air Quality\n'
                                      f'7) 7 Day Forecast')
        else:

            url = f'http://api.openweathermap.org/data/2.5/weather?q={message}&APPID={api_key}&units=metric'
            response = requests.get(url).json()

            if response.get('cod') != 200:
                message = response.get('message', '')
                sendMessage(chat_id, text=f'{message.title()}. Try again!')
            else:
                sendMessage(chat_id, text=f'Here is what you can do:\n'
                                          f'\nType /temp to get the temperature\n'
                                          f'Type /press to get the pressure\n'
                                          f'Type /humidity to get the humidity\n'
                                          f'Type /felt to get the felt temperature\n'
                                          f'Type /windspeed to get the wind speed\n'
                                          f'Type /airquality to get the air quality\n'
                                          f'Type /days to get a seven day forecast')

        return jsonify(r)

    else:
        return '<h1>Welcome to weather app</h1>'

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


@app.route('/days/<city>')
def days(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    google_key = environ.get('GOOGLE_KEY')
    part = 'hourly'
    googleUrl = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_key}'
    googleResponse = requests.get(googleUrl).json()

    result = googleResponse['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']

    latitude = geodata['lat']
    longitude = geodata['lng']

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={part}&appid={api_key}&units=metric'
    response = requests.get(url).json()

    days1 = response.get('daily')[0].get('temp').get('day')
    days2 = response.get('daily')[1].get('temp').get('day')
    days3 = response.get('daily')[2].get('temp').get('day')
    days4 = response.get('daily')[3].get('temp').get('day')
    days5 = response.get('daily')[4].get('temp').get('day')
    days6 = response.get('daily')[5].get('temp').get('day')
    days7 = response.get('daily')[6].get('temp').get('day')

    s = f'{days1} {days2} {days3} {days4} {days5} {days6} {days7}'
    return jsonify(s)


if __name__ == '__main__':

    app.run(debug=True, port=int(environ.get('PORT', 5000)))