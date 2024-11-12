from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app =Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Add new user
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    contact = request.json['contact']
    new_user = User(name, contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


#Get all user
@app.route('/user', methods=['GET'])
def getAllUser():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Show user by ID
@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


#Update user
@app.route('/user/<id>', methods=['PUT'])
def UpdateUser(id):
    user = User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    user.name = name
    user.contact = contact
    db.session.commit()
    return user_schema.jsonify(user)


# Delete user by ID

@app.route('/user/<id>', methods=['DELETE'])
def DeleteUserById(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)