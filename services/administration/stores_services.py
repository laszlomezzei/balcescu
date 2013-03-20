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
mod = Blueprint('stores', __name__)



@mod.route('/service/stores/all')
def getAllStores():
    #todo companyid

    stores = request.db_session.query(Store)\
    .filter(Store.isArchived == False)\
    .filter(Store.parent_id==getCompanyIdForLoggedUser())\
    .all()
    result = transformer.storeTransformer.to_json(stores)
    return jsonify(data=result)


@mod.route('/service/save_store', methods=['POST'])
def saveStore():
    json = request.json
    if json["id"]=="" :
        store = Store()
        request.db_session.add(store)
    else:
        store = request.db_session.query(Store).get(json["id"])


    transformer.storeTransformer.from_json(json,store)
    store.parent_id=getCompanyIdForLoggedUser()
    request.db_session.commit()
    result = transformer.storeTransformer.to_json(store)


    return jsonify(data=result)



@mod.before_request
def before_request():
    request.db_session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.db_session.close()

