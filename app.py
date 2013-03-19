

# standard libraries
import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, jsonify, request, render_template
from flask.views import MethodView


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from database.models import *
from database.migrations import *
from services.json import transformers


## App specific libraries
import settings


#Flask implentation
app = Flask(__name__)
app.debug = True


from services import guidelines_services
app.register_blueprint(guidelines_services.mod)




transformer = transformers.Transformers.getInstance()

#migrations
migrations=[]
migrations.append(Migration001())
migrations.append(Migration002())
migrations.append(Migration003())


session = Session()

schemas = session.query(DatabaseSchema).all()
if len(schemas)==0 :
    schema = DatabaseSchema(0)
    session.add(schema)
    session.commit()
else:
    schema=schemas[0]

#run migrations
for migration in migrations:
    if migration.version>schema.version:
        migration.up(engine)
        schema.version=migration.version
        session.commit()


session.close()






@app.route("/ui/<template>")
def render_ui(template):
    return render_template(template)

@app.route("/inject")
def inject():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # injectData(Session())
    return "Import finished"


@app.route("/cleardb")
def cleardb():
    Base.metadata.drop_all(bind=engine)
    return "Database cleared"




#
# class CanvasAPI(MethodView):
#
#     def post(self, guidelineId):
#         json = request.json
#
#         session = Session()
#         asset = session.query(Asset).get(json["background_id"])
#         canvas = session.query(Canvas).get(json["id"])
#         canvas.backgroundHeight = asset.images[0].imageHeight
#         canvas.backgroundWidth = asset.images[0].imageWidth
#         canvas.backgroundName = asset.images[0].servingURL
#         canvas.backgroundId = asset.images[0].id
#         canvas.imageRatio = float(asset.images[0].imageHeight)/asset.images[0].imageWidth
#
#         #transformer.canvasTransformer.from_json(json,canvas)
#         session.commit()
#         result = transformer.canvasTransformer.to_json(canvas)
#         session.close()
#
#         return jsonify(data=result)




# class GuidelineAPI(MethodView):
    # def get(self, guidelineId):
    #     session = Session()
    #
    #     #load guideline+canvases+hotspots
    #     guideline = session.query(Guideline).filter(Guideline.id==guidelineId).options(
    #         joinedload(
    #             Guideline.canvases,Canvas.hotspots
    #         ),
    #         joinedload(
    #             Guideline.guidelineconversations, GuidelineConversation.store
    #         ),
    #
    #     ).all()
    #
    #
    #     transf = transformer.guidelineTransformer
    #     result =transf.to_json(guideline)
    #     session.close()
    #     return jsonify(data=result)

    # def post(self):
    #     json = request.json
    #
    #     session = Session()
    #     guideline = session.query(Guideline).options(
    #         joinedload(
    #             Guideline.canvases, Canvas.hotspots
    #         )).get(json["id"])
    #     transformer.guidelineTransformer.from_json(json,guideline)
    #     session.commit()
    #     result = transformer.guidelineTransformer.to_json(guideline)
    #     session.close()
    #
    #     return jsonify(data=result)

    # def put(self, guidelineId):
    #
    #     session = Session()
    #     #get guideline
    #     guideline = session.query(Guideline).options(
    #         joinedload(
    #             Guideline.canvases, Canvas.hotspots
    #         )).get(guidelineId)
    #
    #     #create conversations with each store
    #     stores = session.query(Store).all()
    #     for store in stores:
    #         conversation = GuidelineConversation()
    #         store.guidelineconversations.append(conversation)
    #         guideline.guidelineconversations.append(conversation)
    #
    #     guideline.publicationDate=datetime.now()
    #
    #     session.commit()
    #     result = transformer.guidelineTransformer.to_json(guideline)
    #
    #     return jsonify(data=result)






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


# class HotspotAPI(MethodView):
#
#     def post(self, guidelineId, canvasId):
#         json = request.json
#
#         session = Session()
#
#         canvas = session.query(Canvas).get(canvasId)
#         hotspot=Hotspot()
#         transformer.hotspotTransformer.from_json(json,hotspot)
#         canvas.hotspots.append(hotspot)
#         session.commit()
#         result = transformer.hotspotTransformer.to_json(hotspot)
#         session.close()
#
#         return jsonify(data=result)


class PhoneGuidelineAPI(MethodView):

    def get(self):
        session = Session()
        guidelines = session.query(Guideline).options(
            joinedload(
                Guideline.guidelineconversations, GuidelineConversation.store
            ),
            joinedload(
                Guideline.canvases
            ),
            joinedload(
                Guideline.guidelineconversations
            ),
            joinedload(
                Guideline.guidelinefeedbacks
            )

        ).all()

        guidelineIds=[]
        for g in guidelines:
            if not(guidelineIds.__contains__(g.id)):
                guidelineIds.append(g.id)


        #canvases and thumbs
        session.query(Canvas).options(
            joinedload(
                Canvas.hotspots
            )
        ).filter(Canvas.parent_id.in_(guidelineIds)).all()

        #thumbs for conversations
        session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.thumbs
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()

        #feedbacks and users
        session.query(GuidelineFeedback).options(
            joinedload(
                GuidelineFeedback.guidelinefeedbacksphotos
            ),
            joinedload(
                GuidelineFeedback.store
            ),
            joinedload(
                GuidelineFeedback.user
            )
        ).filter(GuidelineFeedback.parent_id.in_(guidelineIds)).all()



        transf = transformer.guidelineTransformer;
        result =transf.to_json(guidelines)
        session.close()
        return jsonify(data=result)






# app.add_url_rule('/service/dashboard/guidelines', view_func=DashboardAPI.as_view('dashboard'))

# app.add_url_rule('/service/guideline/<int:guidelineId>',view_func=GuidelineAPI.as_view('guideline_load'))
# app.add_url_rule('/service/guideline/new',view_func=NewGuidelineAPI.as_view('guideline_new'))
# app.add_url_rule('/service/guideline',view_func=GuidelineAPI.as_view('guideline_update'))
# app.add_url_rule('/service/guideline/<int:guidelineId>',view_func=GuidelineAPI.as_view('guideline_publish'))

#publish guideline
# app.add_url_rule('/service/guideline/<int:guidelineId>/canvas',view_func=CanvasAPI.as_view('canvas'))
# app.add_url_rule('/service/guideline/<int:guidelineId>/canvas/<int:canvasId>/asset',view_func=HotspotAPI.as_view('canvas_asset'))
# app.add_url_rule('',view_func=ConversationAPI.as_view('conversation'))

#phone
app.add_url_rule('/service/guideline/all',view_func=PhoneGuidelineAPI.as_view('phone_guideline'))

#assets
app.add_url_rule('/service/products/all', view_func=ProductsAPI.as_view('products'))
app.add_url_rule('/service/fixtures/all', view_func=FixturesAPI.as_view('fixtures'))
