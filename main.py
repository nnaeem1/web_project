import requests

URL= "https://geocoding-api.open-meteo.com/v1/search"

# parameters: name[city], country, count
params = {
    "name": "Chicago",
    "country": "US",
    "count": 1
}
response = requests.get(URL, params=params, timeout=5)
print(f'Status code: {response.status_code}')
# retrieve the latitude and longitude
latitude = result = response.json()['results'][0]['latitude']
longitude = result = response.json()['results'][0]['longitude']
print(f'Latitude: {latitude}, Longitude: {longitude}')
# #Weather Api
WEATHER_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"
weather_params = {'latitude': latitude, 'longitude': longitude, 'current_weather': True}
weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=10)
print(f'Weather Status Code: {weather_response.status_code}')
weather_data = weather_response.json()
#print(weather_data)
#retrieve the following weather information: city, country, latitude, longitude, temperature, elevation, windspeed, and observation time.

temperature = weather_data['current_weather']['temperature'] #No [0] requried because there isnt multiple outputs and ['current_weather'] tells that temperature and time and windspeed is under it
elevation = weather_data['elevation']
wind_speed = weather_data['current_weather']['windspeed']
observation_time = weather_data['current_weather']['time']
print(f'Temperature: {temperature}, Elevation: {elevation}, Windspeed: {wind_speed}, Time: {observation_time}')

#Convert this into a python object and print it out.
class WeatherInfo:
    def __init__(self, city, country, latitude, longitude, temperature, elevation, wind_speed, observation_time ):
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.elevation = elevation
        self.wind_speed = wind_speed
        self.observation_time = observation_time

    def __str__(self):
        return (f"\n--- Weather Observation ---\n"
                f"City:             {self.city}, {self.country}\n"
                f"Latitude:         {self.latitude}\n"
                f"Longitude:        {self.longitude}\n"
                f"Temperature:      {self.temperature}°C\n"
                f"Elevation:        {self.elevation}m\n"
                f"Windspeed:        {self.wind_speed} km/h\n"
                f"Observation Time: {self.observation_time}")
        

weather_info = WeatherInfo(city = 'Chicago', country="US", latitude=latitude, longitude = longitude, temperature = temperature, elevation = elevation, wind_speed = wind_speed, observation_time = observation_time)
print(weather_info)