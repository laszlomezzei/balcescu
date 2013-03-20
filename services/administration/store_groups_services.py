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
mod = Blueprint('storeGroups', __name__)



@mod.route('/service/store_groups/all')
def getAllStoreGroups():

    stores = request.db_session.query(StoreGroup).filter(StoreGroup.parent_id==getCompanyIdForLoggedUser()).options(
        joinedload(
            StoreGroup.stores
        )
    ).all()

    result = transformer.storeGroupTransformer.to_json(stores)
    return jsonify(data=result)


@mod.route('/service/save_store_group', methods=['POST'])
def saveStoreGroup():
    json = request.json
    if json["id"]=="" :
        sg = StoreGroup()
        request.db_session.add(sg)
    else:
        sg = request.db_session.query(StoreGroup).options(
            joinedload(
                StoreGroup.stores
            )
        ).get(json["id"])

    sg.stores=[]
    transformer.storeGroupTransformer.from_json(json,sg)

    #load all stores it's got now'
    storeList = request.db_session.query(Store).filter(Store.id.in_(sg.storeIds)).all()
    sg.stores=storeList

    request.db_session.commit()
    result = transformer.storeGroupTransformer.to_json(sg)


    return jsonify(data=result)



@mod.before_request
def before_request():
    request.db_session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.db_session.close()

