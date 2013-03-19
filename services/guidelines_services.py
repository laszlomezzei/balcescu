import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request

from database.models import *
from sqlalchemy.orm import joinedload
from json import transformers


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('service', __name__)

@mod.route('/service/dashboard/guidelines')
def getDashboardGuidelines():
    session = Session()
    gl = selectAllGuidelines(session)
    transf = transformer.guidelineFeedbackOverviewTransformer
    result =transf.to_json(gl)
    session.close()
    return jsonify(data=result)


@mod.route('/service/dashboard/conversation/<int:guidelineId>/<int:storeId>')
def getConversations(guidelineId, storeId):
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


@mod.route('/service/guideline/new')
def newGuideline():
    session = Session()

    company = session.query(Company).first()
    guideline = Guideline(name="", description="", dueDate=None)
    company.guidelines.append(guideline)
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


@mod.route('/service/guideline/<int:guidelineId>')
def loadGuideline(guidelineId):
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

@mod.route('/service/guideline', methods=['POST'])
def updateGuideline():
    json = request.json

    session = Session()
    guideline = session.query(Guideline).options(
        joinedload(
            Guideline.canvases, Canvas.hotspots
        )).get(json["id"])
    transformer.guidelineTransformer.from_json(json,guideline)
    session.commit()
    result = transformer.guidelineTransformer.to_json(guideline)
    session.close()

    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>', methods=['PUT'])
def publishGuideline(guidelineId):

    session = Session()
    #get guideline
    guideline = session.query(Guideline).options(
        joinedload(
            Guideline.canvases, Canvas.hotspots
        )).get(guidelineId)

    #create conversations with each store
    stores = session.query(Store).all()
    for store in stores:
        conversation = GuidelineConversation()
        store.guidelineconversations.append(conversation)
        guideline.guidelineconversations.append(conversation)

    guideline.publicationDate=datetime.now()

    session.commit()
    result = transformer.guidelineTransformer.to_json(guideline)

    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>/canvas', methods=['POST'])
def assetToCanvas(guidelineId):
    json = request.json

    session = Session()
    asset = session.query(Asset).get(json["background_id"])
    canvas = session.query(Canvas).get(json["id"])
    canvas.backgroundHeight = asset.images[0].imageHeight
    canvas.backgroundWidth = asset.images[0].imageWidth
    canvas.backgroundName = asset.images[0].servingURL
    canvas.backgroundId = asset.images[0].id
    canvas.imageRatio = float(asset.images[0].imageHeight)/asset.images[0].imageWidth

    session.commit()
    result = transformer.canvasTransformer.to_json(canvas)
    session.close()

    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>/canvas/<int:canvasId>/asset', methods=['POST'])
def assetToHotspot(guidelineId, canvasId):
    json = request.json

    session = Session()

    canvas = session.query(Canvas).get(canvasId)
    hotspot=Hotspot()
    transformer.hotspotTransformer.from_json(json,hotspot)
    canvas.hotspots.append(hotspot)
    session.commit()
    result = transformer.hotspotTransformer.to_json(hotspot)
    session.close()

    return jsonify(data=result)

@mod.route('/service/guideline/all')
def getGuidelinesForPhone():
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



    transf = transformer.guidelineTransformer
    result =transf.to_json(guidelines)
    session.close()
    return jsonify(data=result)





def selectAllGuidelines(session):

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