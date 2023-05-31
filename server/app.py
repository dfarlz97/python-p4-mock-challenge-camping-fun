#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource): 

    def get(self):
        try:
            campers = [c.to_dict(only=("id", "name", "age")) for c in Camper.query.all()]
        
            return campers, 200
        except: 
            return {"error": "404: Camper not found"}
    
    def post(self):
        try:
            new_camper = Camper(
                id=request.json['id'],
                name=request.json['name'],
                age=request.json['age']
            )

            db.session.add(new_camper)
            db.session.commit()

            return new_camper.to_dict(only=("id", "name", "age")), 201
        except:
            return {"error": "400: Validation error"}, 400


api.add_resource(Campers, "/campers")

class Activities(Resource): 

    def get(self):
        try:
             activities = [a.to_dict(only=("id","name","difficulty")) for a in Activity.query.all()]

             return activities, 200
        except: 
             return {"error": "404: Activity not found"}
        
api.add_resource(Activities, "/activities")

class Signups(Resource): 
    
    def post(self):
        try:
            new_signup = Signup(time=request.json['time'],activity_id=request.json['activity_id'],camper_id=request.json['camper_id'],)

            db.session.add(new_signup)
            db.session.commit()

            return new_signup.activity.to_dict(only=("id", "name", "difficulty")), 201
        except: 
            return {"error": "400: Validation error"}

api.add_resource(Signups, "/signups")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
