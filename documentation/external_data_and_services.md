# External data and services
The openAPIs chosen for the realization of this project are:
* [OpenWeatherMap API](https://openweathermap.org/api) 
* [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview)

------------

## OpenWeatherMap API
It is possible to get information about:
* **Temperature**
* **Pressure**
* **Humidity**
* **Felt temperature**
* **Wind speed**

by doing a HTTP request with the GET method to:

```
http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric
```

Instead, **air quality** can be retrieved with a HTTP request and GET method to:

```
http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}
```

It is also possible to get a **seven day forecast** with a HTTP request and GET method to:
```
https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={part}&appid={api_key}&units=metric
```

------------

## Geocoding API
A HTTP request with the GET method to the following URL converts addresses into geographic coordinates,
so that the user can simply type the name of the city of interest to get information on its air quality and on seven-day forecast,
with no need of retrieving its coordinates:


```
https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_key}
``` 

