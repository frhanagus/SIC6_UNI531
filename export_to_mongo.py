from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://wahyum:7nQAAvkVttVRVy3o@tahu.ngvwt.mongodb.net/?retryWrites=true&w=majority&appName=tahu"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

#database set up
db = client['MyDatabase']
my_collections = db["SensorData"]

def store_data(data):
    results = my_collections.insert_one(data)
    print(results.inserted_id)
    return results.inserted_id

@app.route('/sensor1', methods={'POST', 'GET'})
def simpan_data_sensor():
    if request.method == 'POST':
        body = request.get_json()
        # temperature = body['temperature']
        # humidity = body['humidity']
        # timestamp = body['timestamp']
        # data_final =({
        #     "temperature": temperature,
        #     "humidity": humidity
        # })
        if data:
            collection.insert_one(body)  # Insert the data into MongoDB
            return jsonify({"status": "success", "message": "Data saved to MongoDB"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)