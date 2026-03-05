from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():  
    "default route"
    return '<h1>Hello, World! From my first Flask app!</h1>'

@app.route('/about')
def about():
    return 'This is the about page.'

# API Endpoiendpoints: POST(ingest?city=&country=), GET(/observations), GET(/observations/{id}), PUT(/observations/{id}), DELETE(/observations/{id})
@app.route('/ingest', methods=['POST']) #Fetches live weather, saves it, returns record
def ingest_weather():
    return "POST ingest endpoint"

@app.route('/observations', methods=['GET']) #Retrieves all stored observa
def get_all_observation():
    return "All observations"

@app.route('/observations/<int:observation_id>', methods=['GET'])#Retrieves a specific observaƟon by ID
def specific_observation(observation_id):
    return f'Get specific observations {observation_id}'

@app.route('/observations/<int:observation_id>/edit', methods=['PUT'])#Updates the notes field of an observation
def update_observation(observation_id):
    return f'Uppdated observation {observation_id}'

@app.route('/observations/<int:observation_id>/delete', methods=['DELETE'])#Deletes an observaƟon from DB
def delete_observation(observation_id):
    return f'Deleted observation {observation_id}'

if __name__ == '__main__':
    app.run(debug=True)