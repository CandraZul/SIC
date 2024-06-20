from flask import Flask, jsonify
from pymongo import MongoClient
import statistics

app = Flask(__name__)

# MongoDB connection setup
uri = "mongodb+srv://candrazulkarnain8:ql4PUPRJMflmlAxY@cluster0.vqdsd57.mongodb.net/?retryWrites=true&w=majority&tls=true"
client = MongoClient(uri)
db = client.iot

@app.route('/sensor1/<sensor_name>/all', methods=['GET'])
def get_all_sensor_data(sensor_name):
    data = list(db.sensorData.find({}, {"_id": 0, sensor_name: 1, "timestamp": 1}))
    if not data:
        return jsonify({"message": "No data found"}), 404
    # Filter out documents that don't have the requested sensor data
    data = [item for item in data if sensor_name in item]
    return jsonify(data)

@app.route('/sensor1/<sensor_name>/avg', methods=['GET'])
def get_avg_sensor_data(sensor_name):
    data = list(db.sensorData.find({}, {"_id": 0, sensor_name: 1}))
    if not data:
        return jsonify({"average": None})
    # Extract sensor values and filter out documents without the requested sensor data
    values = [item[sensor_name] for item in data if sensor_name in item]
    if not values:
        return jsonify({"average": None})
    avg_value = statistics.mean(values)
    return jsonify({"average": avg_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
