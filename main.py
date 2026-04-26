import requests
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://geocoding-api.open-meteo.com/v1/search"

params = {
    "name": "Karachi", #Insert city name that is deleted
    "country": "PK",  #The country code
    "count": 1
}
response = requests.get(URL, params=params, timeout=5)
print(f'Status code: {response.status_code}')

latitude = response.json()['results'][0]['latitude']
longitude = response.json()['results'][0]['longitude']
print(f'Latitude: {latitude}, Longitude: {longitude}')

WEATHER_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"
weather_params = {'latitude': latitude, 'longitude': longitude, 'current_weather': True}
weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=10)
print(f'Weather Status Code: {weather_response.status_code}')
weather_data = weather_response.json()

temperature = weather_data['current_weather']['temperature']
wind_speed = weather_data['current_weather']['windspeed']
observation_time = weather_data['current_weather']['time']
print(f'Temperature: {temperature}, Windspeed: {wind_speed}, Time: {observation_time}')

connection = psycopg.connect(
    dbname="weather_tracker",
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

cursor.execute("""
    INSERT INTO observations (city, country, latitude, longitude, temperature, windspeed, observation_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", ("Karachi", "PK", latitude, longitude, temperature, wind_speed, observation_time))
    #This too and this
connection.commit()

print("Karachi added back to database")

cursor.close()
connection.close()