from os import environ
import psycopg2
import requests
import telebot
from flask import Flask, request, jsonify, make_response, render_template
from functools import wraps
from flask import Response
from telebot import *
import hashlib

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
        if auth and auth.username == username and hashlib.sha1(bytes(request.authorization.password, encoding='utf-8')).hexdigest() == password:
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
wind_emoji = u'\U0001F32A'
cold_emoji = u'\U0001F976'
faceExhaling_emoji = u'\U0001F62E'
umbrella_emoji = u'\U00002602'
ok_emoji = u'\U0001F44C'
compass_emoji = u'\U0001F9ED'
windblow_emoji = u'\U0001F32C'
calendar_emoji = u'\U0001F4C6'
wink_emoji = u'\U0001F609'
sunglasses_emoji = u'\U0001F60E'

############################


bot_token = environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token, parse_mode=None)

telegramUrl = f'https://api.telegram.org/bot{bot_token}'


def sendMessage(chat_id, text):
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendTemperature(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}°C'
        r = requests.post(tUrl)
        return r.json()


def sendPressure(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} Pa'
        r = requests.post(tUrl)
        return r.json()


def sendHumidity(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} %'
        r = requests.post(tUrl)
        return r.json()


def sendFeltTemp(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}°C'
        r = requests.post(tUrl)
        return r.json()


def sendWindSpeed(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    if 'Error' in text:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text[:-1]}'
        r = requests.post(tUrl)
        return r.json()
    else:
        tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text} km/h'
        r = requests.post(tUrl)
        return r.json()


def sendAirQuality(chat_id, text):
    text = text.replace("'", "").replace("{", "").replace("}", "")
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendDays(chat_id, text):
    text = text.replace("\n", "%0A").replace("'", "").replace("{", "").replace("}","")
    tUrl = telegramUrl + f'/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.post(tUrl)
    return r.json()


def sendAll(chat_id, text):
    text = text.replace("\n", "%0A").replace("'", "").replace("{", "").replace("}","")
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
        elif message == '/temp':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responseTemp = response.get('weather')[0]
            sendTemperature(chat_id, text=str(responseTemp))
        elif message == '/press':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responsePress = response.get('weather')[1]
            sendPressure(chat_id, text=str(responsePress))
        elif message == '/humidity':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responseHum = response.get('weather')[2]
            sendHumidity(chat_id, text=str(responseHum))
        elif message == '/felt':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responseFelt = response.get('weather')[3]
            sendFeltTemp(chat_id, text=str(responseFelt))
        elif message == '/windspeed':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responseWind = response.get('weather')[4]
            sendWindSpeed(chat_id, text=str(responseWind))
        elif message == '/airquality':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()
            responseAqi = response.get('weather')[5]
            sendAirQuality(chat_id, text=str(responseAqi))
        elif message == '/days':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()

            responseDays1 = response.get('weather')[6].get('days')[0]
            responseDays2 = response.get('weather')[6].get('days')[1]
            responseDays3 = response.get('weather')[6].get('days')[2]
            responseDays4 = response.get('weather')[6].get('days')[3]
            responseDays5 = response.get('weather')[6].get('days')[4]
            responseDays6 = response.get('weather')[6].get('days')[5]
            responseDays7 = response.get('weather')[6].get('days')[6]

            string = f'{responseDays1} °C\n{responseDays2} °C\n{responseDays3} °C\n{responseDays4} °C\n{responseDays5} °C\n{responseDays6} °C\n{responseDays7} °C'
            sendDays(chat_id, text=string)
        elif message == '/all':
            message = getValue(chat_id)
            urltwo = f'https://weatherserviceuni.herokuapp.com/telegram/{message}'
            response = requests.get(urltwo).json()

            responseTemp = response.get('weather')[0]
            responsePress = response.get('weather')[1]
            responseHum = response.get('weather')[2]
            responseFelt = response.get('weather')[3]
            responseWind = response.get('weather')[4]
            responseAqi = response.get('weather')[5]
            responseDays1 = response.get('weather')[6].get('days')[0]
            responseDays2 = response.get('weather')[6].get('days')[1]
            responseDays3 = response.get('weather')[6].get('days')[2]
            responseDays4 = response.get('weather')[6].get('days')[3]
            responseDays5 = response.get('weather')[6].get('days')[4]
            responseDays6 = response.get('weather')[6].get('days')[5]
            responseDays7 = response.get('weather')[6].get('days')[6]

            string = f'{responseTemp} °C\n{responsePress} Pa\n{responseHum}/100 \n{responseFelt} °C\n{responseWind} km/h\n'\
                     f'{responseAqi}\n{responseDays1} °C\n{responseDays2} °C\n{responseDays3} °C\n{responseDays4} °C\n'\
                     f'{responseDays5} °C\n{responseDays6} °C\n{responseDays7} °C'
            sendAll(chat_id, text=string)
        elif message == 'start' or message == 'temp' or message == 'press' or message == 'humidity' or message == 'felt'\
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
                                          f'Type /all to get all of the above {sunglasses_emoji}\n\n'
                                          f'If you want to change the city, just type a new one! {wink_emoji}')
                try:
                    insertValue(chat_id, message)
                except psycopg2.Error as e:
                    error = e.pgcode
                    logger.error("FunctionName: %s", error)

        return jsonify(r)

    else:

        if request.authorization and request.authorization.username == username and hashlib.sha1(bytes(request.authorization.password, encoding='utf-8')).hexdigest() == password:
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
    answer = {
            "Temperature": current_temperature
    }
    if current_temperature:
        return make_response(jsonify(answer), 200)
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
    answer = {
        "Pressure": press
    }
    if press:
        return make_response(jsonify(answer), 200)
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
    answer = {
        "Humidity": humidity
    }
    if humidity:
        return make_response(jsonify(answer), 200)
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
    answer = {
        "Felt": feelslike
    }
    if feelslike:
        return make_response(jsonify(answer), 200)
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
    answer = {
        "Wind": windspeed
    }
    if windspeed:
        return make_response(jsonify(answer), 200)
    else:
        return f'Error getting wind speed for {city.title()}'


@app.route('/aqi/<city>')
@auth_required
def aqi(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')

    url_two = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response_two = requests.get(url_two).json()

    if response_two.get('cod') != 200:
        return make_response(f'Error getting air quality for {city.title()}!', 404)
    else:
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
        answer = {
            "Aqi": airquality
        }
        if airquality:
            return make_response(jsonify(answer), 200)
        else:
            return f'Error getting air quality for city: {city.title()}'


@app.route('/days/<city>')
@auth_required
def days(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')

    url_two = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response_two = requests.get(url_two).json()

    if response_two.get('cod') != 200:
        return make_response(f'Error getting a seven-day forecast for {city.title()}!', 404)
    else:
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

        answer = {
            "days": [
                {
                    "Day1": days1
                },
                {
                    "Day2": days2
                },
                {
                    "Day3": days3
                },
                {
                    "Day4": days4
                },
                {
                    "Day5": days5
                },
                {
                    "Day6": days6
                },
                {
                    "Day7": days7
                }
        ]

        }

        return make_response(jsonify(answer), 200)


@app.route('/all/<city>')
@auth_required
def all(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')

    url_two = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response_two = requests.get(url_two).json()

    if response_two.get('cod') != 200:
        return make_response(f'Error getting data for {city.title()}!', 404)
    else:
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

        #s = f'Temperature: {current_temperature} C-' \
        #    f'Pressure: {press} Pa-Humidity: {humidity}/100-Felt temperature: {feelslike} C-Wind Speed: {windspeed} km/h-'

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
        if airquality == 1:
            aq = f'{airquality} (good)'
        elif airquality == 2:
            aq = f'{airquality} (fair)'
        elif airquality == 3:
            aq = f'{airquality} (moderate)'
        elif airquality == 4:
            aq = f'{airquality} (poor)'
        elif airquality == 5:
            aq = f'{airquality} (very poor)'
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

        answer = {
            "weather": [
            {
                "Temperature": current_temperature
            },
            {
                "Pressure": press
            },
            {
                "Humidity": humidity
            },
            {
                "Felt": feelslike
            },
            {
                "Wind": windspeed
            },
            {
                "Aqi": aq
            },
            {
                "days": [
                {
                    "Day1": days1
                },
                {
                    "Day2": days2
                },
                {
                    "Day3": days3
                },
                {
                    "Day4": days4
                },
                {
                    "Day5": days5
                },
                {
                    "Day6": days6
                },
                {
                    "Day7": days7
                }
                ]
            }

        ]

        }


        return make_response(jsonify(answer), 200)


@app.route('/telegram/<city>')
def telegram(city):
    assert city == request.view_args['city']
    api_key = environ.get('API_KEY')

    url_two = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric'
    response_two = requests.get(url_two).json()

    if response_two.get('cod') != 200:
        return make_response(f'Error getting data for {city.title()}!', 404)
    else:
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

        #s = f'Temperature: {current_temperature} C-' \
        #    f'Pressure: {press} Pa-Humidity: {humidity}/100-Felt temperature: {feelslike} C-Wind Speed: {windspeed} km/h-'

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
        if airquality == 1:
            aq = f'{airquality} (good)'
        elif airquality == 2:
            aq = f'{airquality} (fair)'
        elif airquality == 3:
            aq = f'{airquality} (moderate)'
        elif airquality == 4:
            aq = f'{airquality} (poor)'
        elif airquality == 5:
            aq = f'{airquality} (very poor)'
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

        answer = {
            "weather": [
            {
                "Temperature": current_temperature
            },
            {
                "Pressure": press
            },
            {
                "Humidity": humidity
            },
            {
                "Felt": feelslike
            },
            {
                "Wind": windspeed
            },
            {
                "Aqi": aq
            },
            {
                "days": [
                {
                    "Day1": days1
                },
                {
                    "Day2": days2
                },
                {
                    "Day3": days3
                },
                {
                    "Day4": days4
                },
                {
                    "Day5": days5
                },
                {
                    "Day6": days6
                },
                {
                    "Day7": days7
                }
                ]
            }

        ]

        }


        return make_response(jsonify(answer), 200)


if __name__ == '__main__':

    app.run(debug=True, port=int(environ.get('PORT', 5000)))