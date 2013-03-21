import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import jsonify, Blueprint, request

from database.models import *
from sqlalchemy.orm import joinedload, contains_eager
from json import transformers
from commons import *


__author__ = 'danbunea'


transformer = transformers.Transformers.getInstance()
mod = Blueprint('guidelines', __name__)


@mod.before_request
def before_request():
    request.session = Session()



@mod.teardown_request
def teardown_request(exception):
    request.session.close()



@mod.route('/service/dashboard/guidelines')
def getDashboardGuidelines():
    gl = selectAllGuidelines(request.session)
    transf = transformer.guidelineFeedbackOverviewTransformer
    result =transf.to_json(gl)

    return jsonify(data=result)


@mod.route('/service/dashboard/conversation/<int:guidelineId>/<int:storeId>')
def getConversations(guidelineId, storeId):


    #load feedback and store for each
    feedback = request.session.query(GuidelineFeedback).filter(GuidelineFeedback.store_id==storeId).filter(GuidelineFeedback.parent_id==guidelineId).options(
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

    return jsonify(data=result)


@mod.route('/service/guideline/new')
def newGuideline():
    company = request.session.query(Company).first()
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

    request.session.add(guideline)
    request.session.commit()

    transf = transformer.guidelineTransformer
    result =transf.to_json(guideline)

    return jsonify(data=result)


@mod.route('/service/guideline/<int:guidelineId>')
def loadGuideline(guidelineId):


    #load guideline+canvases+hotspots
    guideline = request.session.query(Guideline).filter(Guideline.id==guidelineId).options(
        joinedload(
            Guideline.canvases,Canvas.hotspots
        ),
        joinedload(
            Guideline.guidelineconversations, GuidelineConversation.store
        ),

        ).all()


    transf = transformer.guidelineTransformer
    result =transf.to_json(guideline)

    return jsonify(data=result)

@mod.route('/service/guideline', methods=['POST'])
def updateGuideline():
    json = request.json


    guideline = request.session.query(Guideline).options(
        joinedload(
            Guideline.canvases, Canvas.hotspots
        )).get(json["id"])
    transformer.guidelineTransformer.from_json(json,guideline)
    request.session.commit()
    result = transformer.guidelineTransformer.to_json(guideline)


    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>', methods=['PUT'])
def publishGuideline(guidelineId):


    #get guideline
    guideline = request.session.query(Guideline).options(
        joinedload(
            Guideline.canvases, Canvas.hotspots
        )).get(guidelineId)

    #create conversations with each store
    stores = request.session.query(Store).all()
    for store in stores:
        conversation = GuidelineConversation()
        store.guidelineconversations.append(conversation)
        guideline.guidelineconversations.append(conversation)

    guideline.publicationDate=datetime.now()

    request.session.commit()
    result = transformer.guidelineTransformer.to_json(guideline)

    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>/canvas', methods=['POST'])
def assetToCanvas(guidelineId):
    json = request.json


    asset = request.session.query(Asset).get(json["background_id"])
    canvas = request.session.query(Canvas).get(json["id"])
    canvas.backgroundHeight = asset.images[0].imageHeight
    canvas.backgroundWidth = asset.images[0].imageWidth
    canvas.backgroundName = asset.images[0].servingURL
    canvas.backgroundId = asset.images[0].id
    canvas.imageRatio = float(asset.images[0].imageHeight)/asset.images[0].imageWidth

    request.session.commit()
    result = transformer.canvasTransformer.to_json(canvas)


    return jsonify(data=result)



@mod.route('/service/guideline/<int:guidelineId>/canvas/<int:canvasId>/asset', methods=['POST'])
def assetToHotspot(guidelineId, canvasId):
    json = request.json



    canvas = request.session.query(Canvas).get(canvasId)
    hotspot=Hotspot()
    transformer.hotspotTransformer.from_json(json,hotspot)
    canvas.hotspots.append(hotspot)
    request.session.commit()
    result = transformer.hotspotTransformer.to_json(hotspot)


    return jsonify(data=result)

@mod.route('/service/guideline/all')
def getGuidelinesForPhone():

    guidelines = request.session.query(Guideline).options(
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

    )\
    .all()

    guidelineIds=[]
    for g in guidelines:
        if not(guidelineIds.__contains__(g.id)):
            guidelineIds.append(g.id)


    #canvases and thumbs
    request.session.query(Canvas).options(
        joinedload(
            Canvas.hotspots
        )
    ).filter(Canvas.parent_id.in_(guidelineIds)).all()

    #thumbs for conversations
    request.session.query(GuidelineConversation).options(
        joinedload(
            GuidelineConversation.thumbs
        )
    ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()

    #feedbacks and users
    request.session.query(GuidelineFeedback).options(
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

    return jsonify(data=result)





def selectAllGuidelines(session):

    if isUserInRole('HQ') or isUserInRole('ADMINISTRATOR'):
        guidelines = request.session.query(Guideline)\
        .filter(Guideline.parent_id==getCompanyIdForLoggedUser())\
        .options(
            joinedload(
                Guideline.guidelineconversations
            )
        ).all()

        guidelineIds=[]
        for g in guidelines:
            if not(guidelineIds.__contains__(g.id)):
                guidelineIds.append(g.id)


        #stores for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.store
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()


        #thumbs for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.thumbs
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds)).all()

    if isUserInRole('REGION_HQ'):

        ids = request.session.query(Store.id).filter(Store.store_group_id==getLoggedUser().store_group_id).filter(Store.isArchived==False).all()

        guidelines = request.session.query(Guideline)\
        .filter(Guideline.parent_id==getCompanyIdForLoggedUser())\
        .join(Guideline.guidelineconversations)\
        .options(
            contains_eager(
                Guideline.guidelineconversations
            )
        )\
        .filter(GuidelineConversation.store_id.in_(request.session.query(Store.id).filter(Store.store_group_id==getLoggedUser().store_group_id).filter(Store.isArchived==False)))\
        .all()

        #query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))))

        guidelineIds=[]
        for g in guidelines:
            if not(guidelineIds.__contains__(g.id)):
                guidelineIds.append(g.id)


        #stores for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.store
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds))\
        .filter(Store.store_group_id == getLoggedUser().store_group_id)\
        .all()


        #thumbs for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.thumbs
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds))\
        .filter(GuidelineConversation.store_id == getLoggedUser().store_id)\
        .all()

#        users = request.db_session.query(User)\
#        .join(User.store)\
#        .filter(User.store_id != None)\
#        .filter(User.isArchived == False)\
#        .filter(User.parent_id==getCompanyIdForLoggedUser())\
#        .filter(Store.store_group_id == getLoggedUser().store_group_id)\
#        .all()
#
#        guidelines = request.session.query(Guideline)\
#        .filter(Guideline.parent_id==getCompanyIdForLoggedUser())\
#        .options(
#            joinedload(
#                Guideline.guidelineconversations
#            )
#        )\
#        .filter(GuidelineConversation.store_id == getLoggedUser().store_id)\
#        .all()
    if isUserInRole('STORE_MANAGER'):
        guidelines = request.session.query(Guideline)\
        .filter(Guideline.parent_id==getCompanyIdForLoggedUser())\
        .join(Guideline.guidelineconversations)\
        .options(
            contains_eager(
                Guideline.guidelineconversations, GuidelineConversation.store
            )
        )\
        .filter(GuidelineConversation.store_id == getLoggedUser().store_id)\
        .all()


        guidelineIds=[]
        for g in guidelines:
            if not(guidelineIds.__contains__(g.id)):
                guidelineIds.append(g.id)


        #stores for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.store
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds))\
        .filter(GuidelineConversation.store_id == getLoggedUser().store_id)\
        .all()


        #thumbs for conversations
        gl = request.session.query(GuidelineConversation).options(
            joinedload(
                GuidelineConversation.thumbs
            )
        ).filter(GuidelineConversation.parent_id.in_(guidelineIds))\
        .filter(GuidelineConversation.store_id == getLoggedUser().store_id)\
        .all()




    return guidelines