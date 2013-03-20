__author__ = 'danbunea'

from flask import session

def getLoggedUser():
    return session['loggedUser']

def getCompanyIdForLoggedUser():
    return getLoggedUser().company_id


