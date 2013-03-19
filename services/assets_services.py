import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request

from database.models import *
from sqlalchemy.orm import joinedload
from json import transformers


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('assets', __name__)


@mod.before_request
def before_request():
    request.session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.session.close()


@mod.route('/service/products/all')
def getAllProducts():
    fix = request.session.query(Product).options(
        joinedload(
            Product.images
        )).all()
    result = transformer.productTransformer.to_json(fix)
    return jsonify(data=result)


@mod.route('/service/fixtures/all')
def getAllFixtures():
    fix = request.session.query(Fixture).options(
        joinedload(
            Fixture.images
        )).all()
    result = transformer.fixtureTransformer.to_json(fix)
    return jsonify(data=result)