

# standard libraries
import os
import sys
from inject import injectData


sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, jsonify, url_for, render_template, request
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
#engine = create_engine('mysql+gaerdbms:///'+settings.DATABASE_NAME+'?instance=iss-flasksqlalchemy-shopshape:iss-flasktest-shopshape', echo=True)
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


class ConversationAPI(MethodView):

    def get(self, guidelineId, storeId):
        session = Session()

        #load feedback and store for each
        feedback = session.query(GuidelineFeedback).filter(GuidelineFeedback.store_id==storeId).filter(GuidelineFeedback.parent_id==guidelineId).options(
            joinedload(
                GuidelineFeedback.store
            ),
            joinedload(
                GuidelineFeedback.user
            ),
            joinedload(
                GuidelineFeedback.guidelinefeedbacksphotos
            )
        ).all()


        transf = transformer.guidelineFeedbackTransformer
        result =transf.to_json(feedback)
        session.close()
        return jsonify(data=result)

class GuidelineAPI(MethodView):

    def get(self, guidelineId):
        session = Session()

        #load guideline+canvases+hotspots
        guideline = session.query(Guideline).filter(Guideline.id==guidelineId).options(
            joinedload(
                Guideline.canvases,Canvas.hotspots
            ),
            joinedload(
                Guideline.guidelineconversations, GuidelineConversation.store
            ),

        ).all()


        transf = transformer.guidelineTransformer
        result =transf.to_json(guideline)
        session.close()
        return jsonify(data=result)


class PublishGuidelineAPI(MethodView):

    def get(self):
        session = Session()


        guideline = Guideline(name="", description="", dueDate=None)
        for cnvs in range(5):
            canvas = Canvas(backgroundName = "",
                backgroundId = None,
                backgroundWidth=0,
                backgroundHeight=0,
                imageRatio=1,
                order = cnvs)
            guideline.canvases.append(canvas)

        session.add(guideline)
        session.commit()

        transf = transformer.guidelineTransformer
        result =transf.to_json(guideline)
        session.close()
        return jsonify(data=result)

class CanvasAPI(MethodView):

    def post(self, guidelineId):
        json = request.json

        session = Session()
        canvas = session.query(Canvas).get(json["id"])
        transformer.canvasTransformer.from_json(json,canvas)
        session.commit()
        result = transformer.canvasTransformer.to_json(canvas)
        session.close()

        return jsonify(data=result)



class ProductsAPI(MethodView):

    def get(self):
        session = Session()
        fix = session.query(Product).options(
            joinedload(
                Product.images
            )).all()
        result = transformer.productTransformer.to_json(fix)
        session.close()

        return jsonify(data=result)

class FixturesAPI(MethodView):

    def get(self):
        session = Session()
        fix = session.query(Fixture).options(
            joinedload(
                Fixture.images
            )).all()
        result = transformer.fixtureTransformer.to_json(fix)
        session.close()

        return jsonify(data=result)


class HotspotAPI(MethodView):

    def post(self, guidelineId, canvasId):
        json = request.json

        session = Session()
        canvas = session.query(Canvas).get(json["id"])
        hotspot=Hotspot()
        transformer.hotspotTransformer.from_json(json,hotspot)
        canvas.hotspots.append(hotspot)
        session.commit()
        result = transformer.hotspotTransformer.to_json(hotspot)
        session.close()

        return jsonify(data=result)

app.add_url_rule('/service/dashboard/guidelines', view_func=DashboardAPI.as_view('dashboard'))
app.add_url_rule('/service/products/all', view_func=ProductsAPI.as_view('products'))
app.add_url_rule('/service/fixtures/all', view_func=FixturesAPI.as_view('fixtures'))
app.add_url_rule('/service/guideline/<int:guidelineId>',view_func=GuidelineAPI.as_view('guideline'))
app.add_url_rule('/service/guideline/new',view_func=PublishGuidelineAPI.as_view('publish_guideline'))
app.add_url_rule('/service/guideline/<int:guidelineId>/canvas',view_func=CanvasAPI.as_view('canvas'))
app.add_url_rule('/service/guideline/<int:guidelineId>/canvas/<int:canvasId>/asset',view_func=HotspotAPI.as_view('canvas_asset'))
app.add_url_rule('/service/dashboard/conversation/<int:guidelineId>/<int:storeId>',view_func=ConversationAPI.as_view('conversation'))