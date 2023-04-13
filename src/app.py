"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Starships, Favorites, TokenBlockedList
#from models import Person

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from datetime import date, time, datetime, timezone, timedelta

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_APP_KEY")
jwt = JWTManager(app)

bcrypt = Bcrypt(app) #inicio mi instancia de Bcrypt

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

def verificacionToken(jti):
    jti#Identificador del JWT (es más corto)
    print("jit", jti)
    token = TokenBlockedList.query.filter_by(token=jti).first()

    if token is None:
        return False
    
    return True

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users = list(map(lambda item: item.serialize(), users))
    print(users)

    return jsonify(users), 200 

@app.route('/register', methods=['POST'])
def register_user():
    #recibir el body en json, des-jsonificarlo y almacenarlo en la variable body
    body = request.get_json() #request.json() pero hay que importar request y json

    #ordernar cada uno de los campos recibidos
    email = body["email"]
    name = body["name"]
    password = body["password"]
    is_active = body["is_active"]

    #validaciones
    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=400)
    if "email" not in body:
        raise APIException("You need to specify the email", status_code=400)

    #creada la clase User en la variable new_user
    new_user = User(email=email, name=name, password=password, is_active=is_active)

    #comitear la sesión
    db.session.add(new_user) #agregamos el nuevo usuario a la base de datos
    db.session.commit() #guardamos los cambios en la base de datos

    return jsonify({"mensaje":"User successfully created"}), 201 

@app.route('/get-user/<string:name>', methods=['GET'])
def get_specific_user(name):
    user = User.query.filter_by(name=name).first() 
  
    return jsonify(user.serialize()), 200

@app.route('/get-user', methods=['POST'])
def get_specific_user2():
    body = request.get_json()   
    id = body["id"]

    user = User.query.get(id)   
  
    return jsonify(user.serialize()), 200

@app.route('/get-user', methods=['DELETE'])
def delete_specific_user():
    body = request.get_json()   
    id = body["id"]

    user = User.query.get(id) 

    db.session.delete(user)
    db.session.commit()  
  
    return jsonify("Usuario borrado"), 200

@app.route('/get-user', methods=['PUT'])
def edit_user():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]

    user = User.query.get(id)   
    user.name = name #modifique el nombre del usuario

    db.session.commit()
  
    return jsonify(user.serialize()), 200


###STAR WARS Characters     

@app.route('/add', methods=[ 'POST' ])
def add_people():
    body = request.get_json()
    name = body["name"]
    height = body["height"]
    mass = body["mass"]
    hair_color = body["hair_color"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=400)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=400)
    if  "height" not in body:
        raise APIException("You need to specify the height", status_code=400)
    if  "mass" not in body:
        raise APIException("You need to specify the mass", status_code=400)
    if  "hair_color" not in body:
        raise APIException("You need to specify the hair_color", status_code=400)

    # create a new People object with the data provided
    new_person = People(name=name, height=height, mass=mass, hair_color=hair_color)

    # add the new person to the database and commit changes
    db.session.add(new_person)
    db.session.commit()

    return jsonify({"message": "New character added"}), 201

@app.route('/get-person/<string:name>', methods = [ 'GET' ])
def get_specific_person(name):
    person = People.query.filter_by(name=name).first()
    if person:
        return jsonify(person.serialize()), 200
    else:
        raise APIException('Person not found', status_code=404)

    
@app.route('/edit-person/<string:name>', methods=['PUT'])
def people_edit(name):
    body = request.get_json()   
    new_name = body["name"]
    new_height = body["height"]
    new_mass= body["mass"]
    new_hair_color= body["hair_color"]

    person = People.query.filter_by(name=name).first()  
    person.name = new_name
    person.height = new_height
    person.mass = new_mass
    person.hair_color = new_hair_color


    db.session.commit()
  
    return jsonify(person.serialize()), 200

@app.route('/delete-people', methods=['DELETE'])
def delete_people():
    body = request.get_json()   
    name = body["name"]

    person = People.query.filter_by(name=name).first()
    person.name = name

    db.session.delete(person)
    db.session.commit()  
  
    return jsonify("Character deleted successfully"), 200

### PLANETS     

@app.route('/add-planet', methods=['POST'])
def add_planet():
    body = request.get_json()
    name = body["name"]
    diameter = body["diameter"]
    rotation_period = body["rotation_period"]
    orbital_period = body["orbital_period"]
    gravity = body["gravity"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=400)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=400)
    if  "diameter" not in body:
        raise APIException("You need to specify the diameter", status_code=400)
    if "rotation_period" not in body:
        raise APIException("You need to specify the rotation period", status_code=400)     
    if  "orbital_period" not in body:
        raise APIException("You need to specify the orbital period", status_code=400)
    if  "gravity" not in body:
        raise APIException("You need to specify the gravity", status_code=400)   

    # create a new People object with the data provided
    new_planet = Planets(name=name, diameter=diameter, rotation_period=rotation_period, orbital_period=orbital_period, gravity=gravity)

    # add the new person to the database and commit changes
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"message": "New planet added"}), 201

@app.route('/get-planet/<string:name>', methods = [ 'GET' ])
def get_specific_planet(name):
    planet = Planets.query.filter_by(name=name).first()
    if planet:
        return jsonify(planet.serialize()), 200
    else:
        raise APIException('Planet not found', status_code=404)

@app.route('/edit-planet/<string:name>', methods=['PUT'])
def planet_edit(name):
    body = request.get_json()   
    new_name = body["name"]
    new_diameter = body["diameter"]
    new_rotation_period= body["rotation_period"]
    new_orbital_period= body["orbital_period"]
    new_gravity= body["gravity"]

    planet = Planets.query.filter_by(name=name).first()  
    planet.name = new_name
    planet.diameter = new_diameter
    planet.rotation_period = new_rotation_period
    planet.orbital_period = new_orbital_period
    planet.gravity = new_gravity


    db.session.commit()
  
    return jsonify(planet.serialize()), 200

@app.route('/delete-planet', methods=['DELETE'])
def delete_planet():
    body = request.get_json()   
    name = body["name"]

    planet = Planets.query.filter_by(name=name).first()
    planet.name = name

    db.session.delete(planet)
    db.session.commit()  
  
    return jsonify("Planet deleted successfully"), 200

### STARSHIPS 

@app.route('/add-starship', methods=['POST'])
def add_starship():
    body = request.get_json()
    model = body["model"]
    starship_class = body["starship_class"]
    manufacturer = body["manufacturer"]
    cost_in_credits = body["cost_in_credits"]
    length = body["length"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=400)
    if "model" not in body:
        raise APIException("You need to specify the model", status_code=400)
    if  "starship_class" not in body:
        raise APIException("You need to specify the starship class", status_code=400)
    if "manufacturer" not in body:
        raise APIException("You need to specify the manufacturer", status_code=400)     
    if  "cost_in_credits" not in body:
        raise APIException("You need to specify the cost in credits", status_code=400)
    if  "length" not in body:
        raise APIException("You need to specify the length", status_code=400)   

    # create a new People object with the data provided
    new_starship = Starships(model=model, starship_class=starship_class, manufacturer=manufacturer, cost_in_credits=cost_in_credits, length=length)

    # add the new person to the database and commit changes
    db.session.add(new_starship)
    db.session.commit()

    return jsonify({"message": "New starship added"}), 201

@app.route('/get-starship/<string:name>', methods = [ 'GET' ])
def get_specific_starship(name):
    starship = Starships.query.filter_by(model=name).first()
    if starship:
        return jsonify(starship.serialize()), 200
    else:
        raise APIException('Starship not found', status_code=404)

@app.route('/edit-starship/<string:name>', methods=['PUT'])
def starship_edit(name):
    body = request.get_json()   
    new_model = body["model"]
    new_starship_class = body["starship_class"]
    new_manufacturer= body["manufacturer"]
    new_cost_in_credits= body["cost_in_credits"]
    new_length= body["length"]

    starship = Starships.query.filter_by(model=name).first()  
    starship.model = new_model
    starship.starship_class = new_starship_class
    starship.manufacturer = new_manufacturer
    starship.cost_in_credits = new_cost_in_credits
    starship.length = new_length


    db.session.commit()
  
    return jsonify(starship.serialize()), 200

@app.route('/delete-starship', methods=['DELETE'])
def delete_starship():
    body = request.get_json()   
    model = body["model"]

    starship = Starships.query.filter_by(model=model).first()
    starship.model = model

    db.session.delete(starship)
    db.session.commit()  
  
    return jsonify("Starship deleted successfully"), 200


## **************FAVORITES************

@app.route('/users/<string:name>/favorites', methods=['GET'])
def get_user_favorites(name):
    favorites = Favorites.query.filter_by(user=name).all()
    return jsonify([favorite.serialize() for favorite in favorites])

@app.route('/favorites', methods=['POST'])
def create_favorite():
    data = request.get_json()
    favorite = Favorites (
        user =data['user_name'],
        people =data['people_name'],
        planet =data['planet_name'],
        starship =data['starship_model']
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)