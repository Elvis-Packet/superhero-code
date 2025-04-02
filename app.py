from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superhero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)
@app.route('/')
def home():
    return "Welcome to the Superhero API Structured By one and only ELVIS-PACKET!"


@app.route('/heroes', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def handle_heroes():
    if request.method == 'GET':
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    if request.method == 'POST':
        data = request.get_json()
        try:
            # Ensure all required fields are provided
            if 'name' not in data or 'super_name' not in data:
                return jsonify({"error": "Missing required fields: 'name' and 'super_name'"}), 400

            hero = Hero(
                name=data['name'],
                super_name=data['super_name'],
                superpower=data.get('superpower'),  # Optional field
                superhero_id=data.get('superhero_id')  # Optional field
            )
            db.session.add(hero)
            db.session.commit()
            return jsonify(hero.to_dict()), 201
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'PUT' or request.method == 'PATCH':
        data = request.get_json()
        if 'id' not in data:
            return jsonify({"error": "Missing required field: 'id'"}), 400
        hero = Hero.query.get(data['id'])
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        try:
            hero.name = data.get('name', hero.name)
            db.session.commit()
            return jsonify(hero.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'DELETE':
        data = request.get_json()
        if 'id' not in data:
            return jsonify({"error": "Missing required field: 'id'"}), 400
        hero = Hero.query.get(data['id'])
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        db.session.delete(hero)
        db.session.commit()
        return jsonify({"message": "Hero deleted"}), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def handle_powers():
    if request.method == 'GET':
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    if request.method == 'POST':
        data = request.get_json()
        try:
            power = Power(name=data['name'], description=data['description'])
            db.session.add(power)
            db.session.commit()
            return jsonify(power.to_dict()), 201
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'PUT' or request.method == 'PATCH':
        data = request.get_json()
        power = Power.query.get(data['id'])
        if not power:
            return jsonify({"error": "Power not found"}), 404
        try:
            power.name = data.get('name', power.name)
            power.description = data.get('description', power.description)
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'DELETE':
        data = request.get_json()
        power = Power.query.get(data['id'])
        if not power:
            return jsonify({"error": "Power not found"}), 404
        db.session.delete(power)
        db.session.commit()
        return jsonify({"message": "Power deleted"}), 200

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def handle_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    if request.method == 'GET':
        return jsonify(power.to_dict())

    if request.method == 'PATCH':
        data = request.get_json()
        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

@app.route('/hero_powers', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def handle_hero_powers():
    if request.method == 'GET':
        hero_powers = HeroPower.query.all()
        return jsonify([hero_power.to_dict() for hero_power in hero_powers])

    if request.method == 'POST':
        data = request.get_json()
        try:
            hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )
            db.session.add(hero_power)
            db.session.commit()
            return jsonify(hero_power.to_dict()), 201
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'PUT' or request.method == 'PATCH':
        data = request.get_json()
        hero_power = HeroPower.query.get(data['id'])
        if not hero_power:
            return jsonify({"error": "HeroPower not found"}), 404
        try:
            hero_power.strength = data.get('strength', hero_power.strength)
            hero_power.hero_id = data.get('hero_id', hero_power.hero_id)
            hero_power.power_id = data.get('power_id', hero_power.power_id)
            db.session.commit()
            return jsonify(hero_power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    if request.method == 'DELETE':
        data = request.get_json()
        hero_power = HeroPower.query.get(data['id'])
        if not hero_power:
            return jsonify({"error": "HeroPower not found"}), 404
        db.session.delete(hero_power)
        db.session.commit()
        return jsonify({"message": "HeroPower deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
