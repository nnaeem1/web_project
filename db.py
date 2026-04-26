import os
from dotenv import load_dotenv
import requests
import psycopg
from psycopg import OperationalError

load_dotenv()  # Loads variables from .env file

DB_NAME = "weather_tracker"
DB_USER = os.getenv('db_user')
DB_PASSWORD = os.getenv('db_password')
DB_HOST = "localhost"
DB_PORT = "5432"

cities = [
    ("Karachi", "PK"), ("New York", "US"), ("Tokyo", "JP"), 
    ("Seoul", "KR"), ("Riyadh", "SA"), ("Quito", "EC"), 
    ("Manila", "PH"), ("Mumbai", "IN"), ("Yangon", "MM"), 
    ("Kuala Lumpur", "MY")
]

try:
    connection = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    with connection.cursor() as cursor:

        for city_name, country_code in cities:
            print(f"Fetching data for {city_name}...")
            
            URL = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": city_name,
                "country": country_code,
                "count": 1
            }
            response = requests.get(URL, params=params, timeout=5)
            
            latitude = response.json()['results'][0]['latitude']
            longitude = response.json()['results'][0]['longitude']
            
            WEATHER_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"
            weather_params = {'latitude': latitude, 'longitude': longitude, 'current_weather': True}
            weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=10)
            weather_data = weather_response.json()
            
            temperature = weather_data['current_weather']['temperature']
            windspeed = weather_data['current_weather']['windspeed']
            observation_time = weather_data['current_weather']['time']

            insert_query = """
                INSERT INTO observations 
                (city, country, latitude, longitude, temperature, windspeed, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            
            cursor.execute(insert_query, (
                city_name, 
                country_code, 
                latitude, 
                longitude, 
                temperature, 
                windspeed, 
                observation_time
            ))
            
            connection.commit()
            print(f"Successfully saved {city_name}")

    connection.close() #important to close connection

except OperationalError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

print("Done!")