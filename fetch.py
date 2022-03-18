from flask import Flask, jsonify, request, make_response
from models import db, User,House
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://udneffduzjctjs:931eba260d4f282fb4394218210ddbc684a55e061f3bcf14b2edbae52ac53e03@ec2-3-217-216-13.compute-1.amazonaws.com:5432/d4he6ldo8rg0ns'


db.init_app(app)
manager = Manager(app)
manager.add_command('server',Server)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@app.route('/house', methods=['POST'])
def post_house():
    data=request.get_json()
    new_house = House(
    
    # landlord = data['landlord'],
    location = data['location'],
    description = data['description'],
    pic_path = data['pic_path'],
    price = data['price']
    )
    new_house.save_house()
    return jsonify({'message': 'New house created successfully'})

@app.route('/', methods=['GET'])
def get_all_houses():

    houses = House.query.all()

    output = []

    for house in houses:
        house_data = {}
        house_data['id'] = house.id
        house_data['location'] = house.location
        house_data['description'] = house.description
        house_data['price'] = house.price

        output.append(house_data)

    return jsonify({'houses': output})

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, House=House )

if __name__ == "__main__":
    manager.run()