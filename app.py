

# standard libraries
import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, jsonify
from flask.views import MethodView


import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, inspect, create_engine, Table, Float
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, joinedload, subqueryload
from models import *
import transformers




## App specific libraries
import settings

#database
engine = create_engine('mysql+mysqldb://root@localhost/'+settings.DATABASE_NAME, echo=True)
db_session = scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)


transformer = transformers.Transformers.getInstance()



#Flask implentation
app = Flask(__name__)


#class UserAPI(MethodView):
#
#    def get(self):
#        session = Session()
#        users = session.query(User).all()
#
#
#        transf = transformer.userTransformer;
#        result =transf.to_json(users)
#        session.close()
#        return jsonify(data=result)
#
#
#
#app.add_url_rule('/users', view_func=UserAPI.as_view('user'))

class DashboardAPI(MethodView):

    def get(self):
        session = Session()
        gl = self.select(session)
        transf = transformer.guidelineFeedbackOverviewTransformer;
        result =transf.to_json(gl)
        session.close()
        return jsonify(data=result)

    def select(self,session):

        guidelines = session.query(Guideline).options(
            joinedload(
                Guideline.guidelineconversations
            )
        ).all()

        guidelineIds=[]
        for g in guidelines:
            if not(guidelineIds.__contains__(g.id)):
                guidelineIds.append(g.id)


        #stores for conversations
        gl = session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.store
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()


        #thumbs for conversations
        gl = session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.thumbs
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()



        return guidelines


app.add_url_rule('/dashboard/guidelines', view_func=DashboardAPI.as_view('dashboard'))