from flask import *
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
import os

blueprint = Blueprint("user_api",
                      __name__,
                      template_folder="templates")


@blueprint.route("/api/users")
def get_users():
    session = db_session.create_session()
    if request.method == "GET":
        return jsonify([get_user(i).json for i in range(1, session.query(User).count() + 1)])
    elif request.method == "POST":
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in (rj := request.json) for key in
                     {'address',
                      'position',
                      'speciality',
                      'surname',
                      'name',
                      'login',
                      'age',
                      'password',
                      'city_from'}):
            return jsonify({'error': 'Bad request'})
        elif session.query(Jobs).get(request.json['job_id']):
            return jsonify(error="Id already exists")
        user = User()
        user.address = request.json['address']
        user.position = request.json['position']
        user.speciality = request.json['speciality']
        user.surname = request.json['surname']
        user.name = request.json['name']
        user.email = request.json['login']
        user.city_from = request.json['city_from']
        user.age = int(request.json['age'])
        user.modified_date = datetime.datetime.now()
        user.set_password(request.json['password'])
        session.add(user)
        session.commit()
        return jsonify(success="OK")
    return jsonify(error="Method is not allowed")


@blueprint.route("/api/users/<int:user_id>")
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        user = user.__dict__
        del user["_sa_instance_state"]
        # for k in user.keys():
        #     if '__' in k:
        #         del user[k]
        return jsonify(user)
    else:
        return jsonify(error="Invalid id")


@blueprint.route("/api/edit/<int:user_id>")
def edit_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        user.surname = request.json['surname']
        user.name = request.json['name']
        user.age = request.json['age']
        user.position = request.json['position']
        user.speciality = request.json['speciality']
        user.address = request.json['address']
        user.email = request.json['email']
        if user.city_from != request.json['city_from']:
            os.remove(f"./static/images/{user_id}.png")
            user.city_from = request.json['city_from']
        user.hashed_password = request.json['hashed_password']
        # user.modified_date = request.json['modified_date']
        user.modified_date = datetime.datetime.now()
    else:
        return jsonify(error="Invalid Id")


@blueprint.route("/api/delete/<int:user_id>")
def del_user(user_id):
    session = db_session.create_session()
    us = session.query(User).get(user_id)
    if us:
        for user in session.query(User).filter(User.id > user_id):
            user.id -= 1
        session.commit()
        return jsonify(success="OK")
    return jsonify(error="Invalid id")

