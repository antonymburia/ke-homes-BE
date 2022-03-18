from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['PSQLALCHEMY_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role = db.Column(db.String(255))
    house= db.relationship('House',backref = 'user',lazy="dynamic")
    landlord= db.relationship('Landlord',backref = 'user',lazy="dynamic")
    agent= db.relationship('Agent',backref = 'user',lazy="dynamic")
    def to_json(self):
        return {"username": self.username,
                "email": self.email,
                "role": self.role,
                "house": self.house,
                "landlord": self.landlord,
                "agent": self.agent
                }


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer,primary_key = True)
    agent = db.Column(db.String(255))
    landlord = db.Column(db.String(255))
    location = db.Column(db.Text())
    description = db.Column(db.Text())
    pic_path = db.Column(db.String())
    price = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    landlord= db.relationship('Landlord',backref = 'house',lazy="dynamic")
    agent= db.relationship('Agent',backref = 'house',lazy="dynamic")
    def to_json(self):
        return {"agent": self.agent,
                "landlord": self.landload,
                "location": self.location,
                "pic_path": self.pic_path,
                "price": self.price,
                "landload": self.landlord,
                "agent": self.agent
                }

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer,primary_key = True)
    agent_name = db.Column(db.String (255), index=True)
    house_id = db.Column(db.Integer,db.ForeignKey("houses.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    def to_json(self):
        return {"agent_name": self.agent_name,
                
                }

class Landlord(db.Model):
    __tablename__ = "landlords"
    id=db.Column(db.Integer,primary_key=True)
    landlord_name= db.Column(db.String(255),index=True)
    house_id = db.Column(db.Integer,db.ForeignKey("houses.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    

@app.route('/', methods=['GET'])
def query_records():
    username = request.args.get('username')
    email = request.args.get('email')
    house = request.args.get('house')
    landlord = request.args.get('landload')
    agent = request.args.get('agent')
    user = User.objects(username=username)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

