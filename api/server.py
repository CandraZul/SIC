from flask import Flask, request, jsonify

app = Flask(__name__)

dummy_data = [
    {
        "temperature": 25,
        "humidity": 80,
        "timestamp": "2022-11-25 22:10:00"
    },
    {
        "temperature": 26,
        "humidity": 85,
        "timestamp": "2022-11-25 22:10:05"
    }]

@app.route('/sensor/data', methods=['POST', 'GET'])
def sensor_data():
    if request.method == 'POST':
        data = request.get_json()
        dummy_data.append(data)
        print(data)
        return jsonify({'message': 'Data received!'})
    else:
        return jsonify(dummy_data)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)