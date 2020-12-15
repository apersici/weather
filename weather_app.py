from os import environ
import psycopg2
import requests
import telebot
from flask import Flask, render_template, request, jsonify, make_response
from functools import wraps
from flask import Response
from telebot import *

app = Flask(__name__)

db_host = environ.get('DB_HOST')
database = environ.get('DATABASE')
db_user = environ.get('DB_USER')
db_pass = environ.get('DB_PASSWORD')
db_port = environ.get('DB_PORT')
database_url = environ.get('DATABASE_URL')


try:
    conn = psycopg2.connect(
    host=db_host,
    database=database,
    user=db_user,
    password=db_pass,
    port=db_port)

    print("Database connected")
except:
    Response.status(503)
    print("Database not connected")


def insertValue(chat_id, message):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Cities (CHAT_ID, NAME, NUMBER) VALUES (%s, %s, nextval('cities_increment'))", (chat_id, message))
        conn.commit()
        print("Data inserted succesfully")
        cur.close()
    except psycopg2.Error as e:
        error = e.pgcode
        logger.error("FunctionName: %s", error)


def getValue(chat_id):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT name, number FROM cities WHERE chat_id = {chat_id} ORDER BY number DESC")
        rows = cur.fetchall()

        if rows:
            message = str(rows[0]).split(",")[0].replace("(", "")
            message = message[1:-1]
            return message
        else:
            return 0
        cur.close()
    except psycopg2.Error as e:
        error = e.pgcode
        logger.error("FunctionName: %s", error)


username = environ.get('USERNAME')
password = environ.get('PASSWORD')


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == username and auth.password == password:
            return f(*args, **kwargs)

        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    return decorated


########## EMOJIs ##########

thunderstorm = u'\U0001F4A8'
drizzle = u'\U0001F4A7'
rain = u'\U00002614'
snowflake = u'\U00002744'
snowman = u'\U000026C4'
atmosphere = u'\U0001F301'
clearSky = u'\U00002600'
fewClouds = u'\U000026C5'
clouds = u'\U00002601'
hot = u'\U0001F525'
defaultEmoji = u'\U0001F300'
wind_emoji = u'\U0001F32A'
cold_emoji = u'\U0001F976'
mind_emoji = u'\U0001F92F'
faceExhaling_emoji = u'\U0001F62E'
umbrella_emoji = u'\U00002602'
ok_emoji = u'\U0001F44C'
pressure_emoji = u'\U0001F62C'
compass_emoji = u'\U0001F9ED'
airplane_emoji = u'\U00002708'
windblow_emoji = u'\U0001F32C'
calendar_emoji = u'\U0001F4C6'
wink_emoji = u'\U0001F609'

############################


bot_token = environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode=None)

telegramUrl = f'https://api.telegram.org/bot{bot_token}'


def sendMessage(chat_id, text):
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendTemperature(chat_id, text):
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}°C'
        r = requests.post(tUrl)
        return r.json()


def sendPressure(chat_id, text):
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} Pa'
        r = requests.post(tUrl)
        return r.json()


def sendHumidity(chat_id, text):
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} %'
        r = requests.post(tUrl)
        return r.json()


def sendFeltTemp(chat_id, text):
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}°C'
        r = requests.post(tUrl)
        return r.json()


def sendWindSpeed(chat_id, text):
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} km/h'
        r = requests.post(tUrl)
        return r.json()


def sendAirQuality(chat_id, text):
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendDays(chat_id, text):
    text = text.replace("-", "%0A")
    text = text[1:-1]
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendAll(chat_id, text):
    text = text.replace("-", "%0A")
    text = text[1:-1]
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    api_key = environ.get('API_KEY')
    if request.method == 'POST':
        r = request.get_json()
        first_name = r.get('message').get('chat').get('first_name')
        chat_id = r.get('message').get('chat').get('id')
        message = r.get('message').get('text')

        if message == '/start':
            sendMessage(chat_id, text=f'Hello {first_name}!\nWelcome to WeatherBot {clearSky}\n\nPlease input a city:')
        elif message == '/info':
            sendMessage(chat_id, text=f'You can get information about:\n'
                                      f'1) Temperature {hot}\n'
                                      f'2) Pressure {compass_emoji}\n'
                                      f'3) Humidity {drizzle}\n'
                                      f'4) Felt Temperature {cold_emoji}\n'
                                      f'5) Wind Speed {wind_emoji}\n'
                                      f'6) Air Quality {airplane_emoji}\n'
                                      f'7) 7 Day Forecast {calendar_emoji}\n'
                                      f'8) All of the above {mind_emoji}\n'
                                      f'\nIf you wish to change the city, just type a new one! {wink_emoji}')
        elif message == '/temp':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/temp/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendTemperature(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/press':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/temp/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendPressure(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/humidity':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/humidity/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendHumidity(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/felt':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/feelslike/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendFeltTemp(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/windspeed':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/wind/speed/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendWindSpeed(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/airquality':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/aqi/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendAirQuality(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/days':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/days/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendDays(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == '/all':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/all/{message}'
            response = requests.get(urltwo, auth=(username, password))
            response2 = response.content
            sendAll(chat_id, text='' + response2.decode('utf-8').replace("\n", ""))
        elif message == 'start' or message == 'info' or message == 'temp' or message == 'press' or message == 'humidity' or message == 'felt'\
                or message == 'windspeed' or message == 'airquality' or message == 'days' or message == 'all':
            sendMessage(chat_id, text=f'City not found. Try again!')
        else:

            url = f'http://api.openweathermap.org/data/2.5/weather?q={message}&APPID={api_key}&units=metric'
            response = requests.get(url).json()

            if response.get('cod') != 200:
                message = response.get('message', '')
                sendMessage(chat_id, text=f'{message.title()}. Try again!')
            else:
                sendMessage(chat_id, text=f'{message} it is then! {ok_emoji}\n'
                                          f'\nHere is what you can do:\n'
                                          f'\nType /temp to get the temperature {hot} in {message}\n'
                                          f'Type /press to get the pressure {compass_emoji} in {message}\n'
                                          f'Type /humidity to get the humidity {drizzle} in {message}\n'
                                          f'Type /felt to get the felt temperature {cold_emoji}  in {message}\n'
                                          f'Type /windspeed to get the wind speed {wind_emoji} in {message}\n'
                                          f'Type /airquality to get the air quality {windblow_emoji} in {message}\n'
                                          f'Type /days to get a seven day forecast {calendar_emoji} for {message}\n'
                                          f'Type /all to get all of the above {mind_emoji}')
                try:
                    insertValue(chat_id, message)
                except psycopg2.Error as e:
                    error = e.pgcode
                    logger.error("FunctionName: %s", error)

        return jsonify(r)

    else:

        if request.authorization and request.authorization.username == username and request.authorization.password == password:
            return '<h1>You are logged in</h1>'

        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/temp/<city>')
@auth_required
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
@auth_required
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
@auth_required
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


@app.route('/feelslike/<city>')
@auth_required
def feelslike(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return make_response(f'Error getting felt temperature for {city.title()}!', 404)

    feelslike = response.get('main', {}).get('feels_like')
    if feelslike:
        return jsonify(feelslike)
    else:
        return f'Error getting felt temperature for {city.title()}'


@app.route('/wind/speed/<city>')
@auth_required
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
@auth_required
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
@auth_required
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

    s = f'Day1: {days1} C-Day2: {days2} C-Day3: {days3} C-Day4: {days4} C-Day5: {days5} C-Day6: {days6} C-Day7: {days7} C'
    return jsonify(s)


@app.route('/all/<city>')
@auth_required
def all(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')
    google_key = environ.get('GOOGLE_KEY')
    part = 'hourly'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response = requests.get(url).json()

    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message})'

    current_temperature = response.get('main', {}).get('temp')
    press = response.get('main', {}).get('pressure')
    humidity = response.get('main', {}).get('humidity')
    feelslike = response.get('main', {}).get('feels_like')
    windspeed = response.get('wind', {}).get('speed')

    s = f'Temperature: {current_temperature} C-' \
        f'Pressure: {press} Pa-Humidity: {humidity}/100-Felt temperature: {feelslike} C-Wind Speed: {windspeed} km/h-'

    googleUrl = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_key}'
    googleResponse = requests.get(googleUrl).json()

    result = googleResponse['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']

    latitude = geodata['lat']
    longitude = geodata['lng']

    urlPollution = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}'
    responsePollution = requests.get(urlPollution).json()

    airquality = responsePollution.get('list')[0].get('main', {}).get('aqi')
    if airquality:
            s = s + f'Air quality: {airquality}-'
    else:
        return f'Error getting air quality for city: {city}'

    urlOneCall = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={part}&appid={api_key}&units=metric'
    responseOneCall = requests.get(urlOneCall).json()

    days1 = responseOneCall.get('daily')[0].get('temp').get('day')
    days2 = responseOneCall.get('daily')[1].get('temp').get('day')
    days3 = responseOneCall.get('daily')[2].get('temp').get('day')
    days4 = responseOneCall.get('daily')[3].get('temp').get('day')
    days5 = responseOneCall.get('daily')[4].get('temp').get('day')
    days6 = responseOneCall.get('daily')[5].get('temp').get('day')
    days7 = responseOneCall.get('daily')[6].get('temp').get('day')

    s = s + f'-Day1: {days1} C-Day2: {days2} C-Day3: {days3} C-Day4: {days4} C-Day5: {days5} C-Day6: {days6} C-Day7: {days7} C'

    return jsonify(s)


if __name__ == '__main__':

    app.run(debug=True, port=int(environ.get('PORT', 5000)))