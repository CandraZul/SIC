from flask import Flask, request, jsonify
from datetime import datetime
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://candrazulkarnain8:ql4PUPRJMflmlAxY@cluster0.vqdsd57.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.iot

app = Flask(__name__)

def generate_dummy_data():
    return {
        "temperature"   : random.randint(20, 40),
        "humidity"      : random.randint(0, 100),
        "timestamp"     : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
@app.route('/sensor1', methods=['POST', 'GET'])
def sensor_data():
    if request.method == 'POST':
        database = generate_dummy_data()
        db.sensorData.insert_one(database)
        return jsonify({'message': 'Data received!'})
    else:
        return jsonify(generate_dummy_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)