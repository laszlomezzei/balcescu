__author__ = 'danbunea'

from flask import session

def getLoggedUser():
    return session['loggedUser']

def getCompanyIdForLoggedUser():
    return getLoggedUser().parent_id


def isUserInRole(role):
    return getLoggedUser().roles == role