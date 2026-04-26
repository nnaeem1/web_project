from flask import Flask, render_template, request, redirect, url_for
import psycopg
from psycopg import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_NAME = "weather_tracker"
DB_USER = os.getenv('db_user')
DB_PASSWORD = os.getenv('db_password')
DB_HOST = "localhost"
DB_PORT = "5432"

@app.route('/')
def home():  
    "default route"
    return '<h1>Hello, World! From my first Flask app!</h1>'

@app.route('/observations', methods=['GET'])#Retrieves all stored observations
def get_all_observation():
    """Retrieves all stored observations"""
    try:
        connection = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT observation_id, city, country, temperature, windspeed, observation_time
            FROM observations 
            ORDER BY observation_id
        """)
        
        observations = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('observations.html', observations=observations)
        
    except OperationalError as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/observations/<int:observation_id>', methods=['GET'])#Retrieves a specific observation by ID
def specific_observation(observation_id):
    """Retrieves a specific observation by ID"""
    try:
        connection = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT observation_id, city, country, latitude, longitude, 
                   temperature, windspeed, observation_time, notes, created_at
            FROM observations 
            WHERE observation_id = %s
        """, (observation_id,))
        
        observation = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if observation:
            return render_template('observation_detail.html', observation=observation)
        else:
            return f"Observation with ID {observation_id} not found", 404
        
    except OperationalError as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/observations/<int:observation_id>/edit', methods=['POST'])#Updates the notes part of an observation
def update_observation(observation_id):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        
        notes = request.form.get('notes')
        
        cursor.execute("""
            UPDATE observations 
            SET notes = %s 
            WHERE observation_id = %s
        """, (notes, observation_id))
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return redirect(url_for('specific_observation', observation_id=observation_id))
        
    except OperationalError as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/observations/<int:observation_id>/delete', methods=['POST'])#Deletes an observation
def delete_observation(observation_id):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM observations WHERE observation_id = %s", (observation_id,))
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return redirect(url_for('get_all_observation'))
        
    except OperationalError as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)