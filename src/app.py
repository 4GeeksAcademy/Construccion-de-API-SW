import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

CURRENT_USER_ID = 1


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.get_all()
    return jsonify([u.serialize() for u in users]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favs = Favorite.get_by_user(CURRENT_USER_ID)
    return jsonify([f.serialize() for f in favs]), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    chars = Character.get_all()
    return jsonify([c.serialize() for c in chars]), 200


@app.route('/characters/<int:char_id>', methods=['GET'])
def get_single_character(char_id):
    char = Character.get_by_id(char_id)
    if char is None:
        raise APIException("Character not found", 404)
    return jsonify(char.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.get_all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.get_by_id(planet_id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.get_all()
    return jsonify([v.serialize() for v in vehicles]), 200


@app.route('/vehicles/<int:veh_id>', methods=['GET'])
def get_single_vehicle(veh_id):
    veh = Vehicle.get_by_id(veh_id)
    if veh is None:
        raise APIException("Vehicle not found", 404)
    return jsonify(veh.serialize()), 200


@app.route('/favorite/character/<int:char_id>', methods=['POST'])
def add_favorite_character(char_id):
    if Character.get_by_id(char_id) is None:
        raise APIException("Character not found", 404)

    if Favorite.find(CURRENT_USER_ID, char_id=char_id):
        raise APIException("Already in favorites", 400)

    fav = Favorite(user_id=CURRENT_USER_ID, character_id=char_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    if Planet.get_by_id(planet_id) is None:
        raise APIException("Planet not found", 404)

    if Favorite.find(CURRENT_USER_ID, planet_id=planet_id):
        raise APIException("Already in favorites", 400)

    fav = Favorite(user_id=CURRENT_USER_ID, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    if Vehicle.get_by_id(vehicle_id) is None:
        raise APIException("Vehicle not found", 404)

    if Favorite.find(CURRENT_USER_ID, vehicle_id=vehicle_id):
        raise APIException("Already in favorites", 400)

    fav = Favorite(user_id=CURRENT_USER_ID, vehicle_id=vehicle_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201


@app.route('/favorite/character/<int:char_id>', methods=['DELETE'])
def delete_favorite_character(char_id):
    fav = Favorite.find(CURRENT_USER_ID, char_id=char_id)
    if fav is None:
        raise APIException("Favorite not found", 404)

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Character removed"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = Favorite.find(CURRENT_USER_ID, planet_id=planet_id)
    if fav is None:
        raise APIException("Favorite not found", 404)

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Planet removed"}), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    fav = Favorite.find(CURRENT_USER_ID, vehicle_id=vehicle_id)
    if fav is None:
        raise APIException("Favorite not found", 404)

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Vehicle removed"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
