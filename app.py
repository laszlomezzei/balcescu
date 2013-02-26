

# standard libraries
import os
import sys
from inject import injectData


sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, jsonify, url_for, render_template
from flask.views import MethodView


import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, inspect, create_engine, Table, Float
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, joinedload, subqueryload
from models import *
import transformers



## App specific libraries
import settings

#database
#engine = create_engine('mysql+mysqldb://root@localhost/'+settings.DATABASE_NAME, echo=True)
engine = create_engine('mysql+gaerdbms:///'+settings.DATABASE_NAME+'?instance=iss-flasksqlalchemy-shopshape:iss-flasktest-shopshape', echo=True)
#engine.url.username="root"

db_session = scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)


transformer = transformers.Transformers.getInstance()



#Flask implentation
app = Flask(__name__)

@app.route("/inject")
def inject():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    injectData(Session())
    return "Import finished"


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


app.add_url_rule('/service/dashboard/guidelines', view_func=DashboardAPI.as_view('dashboard'))
