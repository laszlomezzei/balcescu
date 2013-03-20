__author__ = 'danbunea'


import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request, flash, redirect, url_for, session, current_app

from database.models import *
from sqlalchemy.orm import joinedload
from json import transformers


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('service', __name__)


@mod.before_request
def before_request():
    request.db_session = Session()


@mod.teardown_request
def teardown_request(exception):
    request.db_session.close()



@mod.route('/service/login', methods=['POST'])
def login():
    required = ['username','password']
    for r in required:
        if r not in request.form:
            flash("Error {0} is required.".format(r))
            return redirect(url_for('/'))
    usr=request.form['username']
    pwd=request.form['password']

    current_app.logger.debug(usr+" "+pwd)

    user = request.db_session.query(User).filter(User.email==usr).filter(User.password==pwd).first()
    if user == None :
        flash("Username or password are wrong.")
        current_app.logger.debug("Username or password are wrong.")
        return redirect(url_for('/'))

    session['loggedUser'] = user
    current_app.logger.debug("Tutto bene")
    return redirect('/ui/guidelines.html')
