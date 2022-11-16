from crypt import methods
from flask import Flask, jsonify, request
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)
app.config.from_envvar("ENV_FILE_LOCATION")
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/midterm_heart"
}
initialize_db(app)
initialize_routes(api)

heart_records = [
    {
        "heart_id": 1,
        "date": "March 12, 2022",
        "heart_rate": 90,
    },
    {

        "heart_id": 2,
        "date": "March 13, 2022",
        "heart_rate": 80
    }
]

@jwt_required
@app.route('/records', methods=['GET'])
def getHeartData():
    return jsonify(heart_records)

@jwt_required
@app.route('/records/<int:heart_id>', methods=['GET'])
def getSpecificHeartData(heart_id):
    record = [ record for record in heart_records if record['heart_id'] == heart_id ]
    return jsonify(record)

@jwt_required
@app.route('/records/add', methods=['POST'])
def addHeartData():
    records = request.get_json()
    heart_records.append(records)
    return {'heart_id': len(heart_records)},200

@jwt_required
@app.route('/delete_records/<int:heart_id>', methods=['DELETE'])
def deleteHeartData(heart_id):
    record = [ record for record in heart_records if record['heart_id'] == heart_id ]
    heart_records.remove(record[0])

    return jsonify(heart_records),200

@jwt_required
@app.route('/update_records/<int:heart_id>', methods=['PUT'])
def updateHeartData(heart_id):
    record = [ record for record in heart_records if record['heart_id'] == heart_id ]
    record[0]['heart_rate'] = request.json['heart_rate']
    return jsonify(heart_records)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)