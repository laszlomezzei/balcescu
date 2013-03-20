__author__ = 'danbunea'
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request

from database.models import *
from sqlalchemy.orm import joinedload
from services.json import transformers


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('users', __name__)



@mod.route('/service/users/all')
def getAllUsers():
    #todo companyid
    users = request.db_session.query(User).filter(User.store_id == None).all()
    result = transformer.userTransformer.to_json(users)
    return jsonify(data=result)


@mod.route('/service/store_users/all')
def getAllStoreUsers():
    #todo companyid
    users = request.db_session.query(User).filter(User.store_id != None).all()
    result = transformer.userTransformer.to_json(users)
    return jsonify(data=result)

@mod.route('/service/save_user', methods=['POST'])
def saveUser():
    json = request.json
    if json["id"]=="" :
        user = User()
        request.db_session.add(user)
    else:
        store = request.db_session.query(User).get(json["id"])


    transformer.usersTransformer.from_json(json,user)

    request.db_session.commit()
    result = transformer.userTransformer.to_json(user)


    return jsonify(data=result)



@mod.before_request
def before_request():
    request.db_session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.db_session.close()

