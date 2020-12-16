# Deploy
The app was deployed to [Heroku](http://heroku.com),
which is automatically synced with the branch *master* of this GitHub repository.

------------

## Variables
The app uses a series of private variables in order to guarantee additional security.

The following variables were used:

* **API_KEY**: OpenWeatherMap API key, needed to get data
* **BOT_TOKEN**: Telegram bot token
* **GOOGLE_KEY**: Google API key, needed to get data
* **USERNAME**: username required for the authentication to the webservice
* **PASSWORD**: password required for the authentication to the webservice
* **DATABASE**: database name
* **DB_USER**: database user
* **DB_PASSWORD**: database password
* **DATABASE_URI**: database URI
* **DB_HOST**: database host
* **DB_PORT**: database port


------------

## Telegram webhook
The webhook was set following this guide: [Setting the webhook](https://core.telegram.org/bots/api#setwebhook).