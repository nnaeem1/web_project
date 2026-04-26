 # **Weather App**


## 1. Features 
- Fetches weather data from Open-Meteo API
- Stores data in PostgreSQL database
- View all weather observations in a table 
- View detailed weather obsertaions for each city
- Add and edit notes for each observation
- Delete observations

## 2. Installation
Required Software:
- requests 
- psycopg
- pythton-dotenv
- PostgreSQL

## 3. Setting up

Create a database and name it weather_tracker or something similar

Then open pgAdmin and run:

CREATE TABLE observations (
    observation_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    temperature DECIMAL,
    windspeed DECIMAL,
    observation_time TIMESTAMP NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

## 4. Environment 

Create a .env file in your project folder with:
db_user = postgres
db_password= your password

## 5. Usage

1. Run db.py
2. Run app.py
3. Navigate to http://127.0.0.1:5000/observations
4. Specific city can be viewed by: http://127.0.0.1:5000/observations/3
5. To add note, go to a city detail page and type in the box at the bottom.
6. To delete a city, click the red button
7. A deleted city can be added back using main.py. Just update it with the city name and country and run:
python main.py