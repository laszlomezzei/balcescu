__author__ = 'danbunea'
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request

from database.models import *
from sqlalchemy.orm import joinedload
from services.json import transformers
from services.commons import *


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('users', __name__)



@mod.route('/service/users/all')
def getAllUsers():

    getCompanyIdForLoggedUser()
    users = request.db_session.query(User)\
        .filter(User.roles != 'STORE') \
        .filter(User.isArchived == False) \
        .filter(User.parent_id==getCompanyIdForLoggedUser())\
        .all()
    result = transformer.userTransformer.to_json(users)
    return jsonify(data=result)


@mod.route('/service/storeusers/all')
def getAllStoreUsers():
    if isUserInRole('HQ') or isUserInRole('ADMINISTRATOR'):
        users = request.db_session.query(User)\
            .filter(User.store_id != None)\
            .filter(User.isArchived == False)\
            .filter(User.parent_id==getCompanyIdForLoggedUser())\
            .all()
    if isUserInRole('REGION_HQ'):
        users = request.db_session.query(User)\
            .join(User.store)\
            .filter(User.store_id != None)\
            .filter(User.isArchived == False)\
            .filter(User.parent_id==getCompanyIdForLoggedUser())\
            .filter(Store.store_group_id == getLoggedUser().store_group_id)\
            .all()
    if isUserInRole('STORE_MANAGER'):
        users = request.db_session.query(User)\
            .filter(User.store_id == getLoggedUser().store_id)\
            .filter(User.isArchived == False)\
            .filter(User.parent_id==getCompanyIdForLoggedUser())\
        .all()
    result = transformer.userTransformer.to_json(users)
    return jsonify(data=result)

@mod.route('/service/save_user', methods=['POST'])
def saveUser():
    json = request.json
    if json["id"]=="" :
        user = User()
        request.db_session.add(user)
    else:
        user = request.db_session.query(User).get(json["id"])


    transformer.userTransformer.from_json(json,user)
    user.parent_id = getCompanyIdForLoggedUser()
    request.db_session.commit()
    result = transformer.userTransformer.to_json(user)


    return jsonify(data=result)



@mod.before_request
def before_request():
    request.db_session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.db_session.close()

