"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('FLASK_APP_KEY')
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

def swapi_to_localhost(swapi_url):
    return swapi_url.replace("https://www.swapi.tech/api/", "https://3000-gold-canidae-6ovungq4.ws-us25.gitpod.io/")



# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def handle_people():
    response = requests.get('https://www.swapi.tech/api/people?page=1&limit=1000')
    response = response.json()

    results = response['results']

    for result in results:

        result.update(url= swapi_to_localhost(result["url"]))

    return jsonify(results), 200



# esta ruta trae todos los planetas
@app.route('/planets', methods=['GET'])
def handle_planet():
    # consultar la api de Star Wars
    response = requests.get('https://www.swapi.tech/api/planets?page=1&limit=1000')
    response = response.json()

    results = response['results']

    for result in results:
        
        result.update(url= swapi_to_localhost(result["url"]))

    return jsonify(results), 200


@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    response = requests.get('https://www.swapi.tech/api/vehicles?page=1&limit=1000')
    response = response.json()

    results = response['results']

    for result in results:

        result.update(url= swapi_to_localhost(result["url"]))

    return jsonify(results), 200


@app.route('/singup', methods=['POST'])
def handle_singup():
    body = request.json
    new_user = User.create(body)
    if new_user is not None:
        return jsonify(new_user.serialize()), 201
    else:
        return jsonify({"message": "use was not created"}), 500


@app.route('/singin', methods=['POST'])
def handle_singin():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email= email, password= password).one_or_none()
    if user is not None:
        token = create_access_token(identity= user.id)
        return jsonify({"token": token, "user_id": user.id}), 200
    else:
        return jsonify({"message": "bad credentials"}), 401


@app.route('/favorites', methods=['GET'])
@jwt_required()
def handle_get_favorites():
    user_id= get_jwt_identity()
    favorites_get= Favorite.query.filter_by(user_id= user_id)
    response = []
    for favorite in favorites_get:
        response.append(favorite.serialize())
    return jsonify(response), 200


@app.route('/favorites/<string:nature>', methods=['POST'])
@jwt_required()
def handle_favorites(nature):
    uid = request.json["uid"]
    name = request.json["name"]
    # user_id = request.json["user_id"]
    new_favorite = Favorite(
        user_id = get_jwt_identity(),
        name = name,
        url = f"https://www.swapi.tech/api/{nature}/{uid}" 
    )
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    except Exception as error:
        db.session.rollback()
        return jsonify(error.args), 500


@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def handle_fav_delete(favorite_id):
    favorite = Favorite.query.filter_by(id= favorite_id).one_or_none()
    if favorite is not None:
        favorite_delete = favorite.delete()
        if favorite_delete == True:
            return jsonify([]), 204
        else:
            return jsonify({"message":"not cleared, please try again"}), 500
    else:
        return jsonify({"message":"not found"}), 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
