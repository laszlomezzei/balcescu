

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
import json
import webapp2
from inject import *
import transformers




## App specific libraries
import settings





#engine = create_engine('sqlite:///tutorial.db')
engine = create_engine('mysql+mysqldb://root@localhost/'+settings.DATABASE_NAME, echo=True)
db_session = scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)






class MainHandler(webapp2.RequestHandler):

    def get(self):
        init_db()
        #injectData()



def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def new_alchemy_encoder(revisit_self = False, fields_to_expand = []):
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            #print obj.__class__
            if isinstance(obj, sqlalchemy.orm.query.Query):
                #print "here"
                return None


            if isinstance(obj, Base):

                fields = {}

                for field in obj.__table__.columns:
                    print field
                    val = obj.__getattribute__(field.name)
                    fields[field.name] = val



                for field in fields_to_expand:

                    if hasattr(obj, field):
                        val = obj.__getattribute__(field)
                        #if it is list
                        if (isinstance(val, list) and len(val) > 0 and isinstance(val[0], Base)):
                            fields[field] = val
                        #print field
                        if isinstance(val,Base):
                            print field
                            #fields[field] = val

                return fields





            if hasattr(obj, 'isoformat'): #handles both date and datetime objects
                return obj.isoformat()



            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder


class SelectGuidelineHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        session = Session()
        guidelines = select(session)
#        print guidelines
#        jsonx=json.dumps({"results":guidelines[0]}, cls=new_alchemy_encoder(False, ['guidelineconversations', 'Store']), check_circular=False  )
        #print jsonx
        #json.dump(jsonx, self.response.out)

        transf = transformers.GuidelineFeedbackOverviewTransformer()
        result =transf.to_json(guidelines)
        session.close()
        self.response.out.write(result)





def select(session):



    gl = session.query(GuidelineConversation).options(
        joinedload(
            GuidelineConversation.store
        )
    ).all()

    gl = session.query(GuidelineConversation).options(
        joinedload(
            GuidelineConversation.guideline
        )
    ).all()

    gl = session.query(GuidelineConversation).options(
        joinedload(
            GuidelineConversation.thumbs
        )
    ).all()


    gl = session.query(Guideline).options(
        joinedload(
            Guideline.guidelineconversations
        )
    ).all()
    return gl

#    guidelines=[]
#    for conv in gl:
#        if not(guidelines.__contains__(conv.guideline)):
#            guidelines.append(conv.guideline)
#
#    return guidelines

def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def injectData():
    #self.response.headers['Content-Type'] = 'application/json'
    #json.dump({"name":company.name}, self.response.out)

    # Create company
    company = Company(name = "VR")

    # Create stores
    storeRo = Store(name="VR Romania", address="Pta Balcescu 4/6, Timisoara")
    storeNl = Store(name="VR Nederland", address="Ruyterkade 6, Amsterdam")
    company.stores=[storeRo, storeNl]

    # Create HQ Users
    u1 = User(email="marten", username="Marten HQ", password="1234", roles='["ROLE_USER", "HQ"]')
    u2 = User(email="dan", username="Dan HQ", password="1234",roles='["ROLE_USER","HQ"]')
    u3 = User(email="laci", username="Laszlo HQ", password="1234",roles='["ROLE_USER","HQ"]')
    company.users=[u1,u2,u3]

    # Create STORE Users
    u4 = User(email="marten_store", username="Marten Store", password="1234",roles='["ROLE_USER","STORE"]')
    storeNl.users=[u4]
    u5 = User(email="dan_store", username="Dan Store", password="1234",roles='["ROLE_USER","STORE"]')
    u6 = User(email="laci_store", username="Laszlo Store", password="1234",roles='["ROLE_USER","STORE"]')
    storeRo.users = [u5,u6]
    company.users=[u1,u2,u3,u4,u5,u6]

    # Create Tag Group
    tg1 = TagGroup(name="Optional")
    tg2 = TagGroup(name="Brand", mandatoryProduct=True, tags=[Tag(name="Adidas"),Tag(name="Nike"),Tag(name="Puma")])
    company.taggroups = [tg1, tg2]

    # upload images
    i1 = uploadImage("img1.png")
    i2 = uploadImage("dashboard_dummy_thumb_1.png")
    i3 = uploadImage("dashboard_dummy_thumb_2.png")
    i4 = uploadImage("dashboard_dummy_thumb_3.png")
    i5 = uploadImage("dashboard_dummy_thumb_4.png")
    i6 = uploadImage("dashboard_dummy_thumb_5.png")
    i7 = uploadImage("fixture1.png")
    i8 = uploadImage("product1.png")
    i9 = uploadImage("product2.png")
    i10 = uploadImage("product3.png")
    company.images = [i1,i2,i3,i4,i5,i6,i7,i8,i9,i10]

    # Create fixtures
    f1 = Fixture(name="Fixture 1", search_name="fixture 1", fixtureId="1234", search_fixtureId="1234", images=[i7]) #
    company.fixtures = [f1]

    # Create products
    p1 = Product(name="Product 1", productId="1", images=[i8])
    p2 = Product(name="Product 2", productId="2", images=[i9])
    p3 = Product(name="Product 3", productId="3", images=[i10])
    company.products = [p1,p2,p3]


    # save company
    sess = Session()
    sess.add(company)
    sess.commit()


    # Create guidelines and feedbacks

    dueDate = date.today()+timedelta(days=5)

    g1 = Guideline(name="Guideline 1", description="Description for Guideline 1", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g1, i7, [p1,p2],[storeRo,storeNl], 1)
    company.guidelines.append(g1)
    addGuidelineFeedback(storeRo, g1, u6, "Feedback from store", [i2])
    addGuidelineFeedback(storeNl, g1, u4, "Feedback from store", [i6])


    g2 = Guideline(name="Guideline 2", description="Description for Guideline 2", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g2, i7, [p1],[storeRo, storeNl], 1)
    company.guidelines.append(g2)
    addGuidelineFeedback(storeRo, g2, u5, "Feedback from store", [i3])
    addGuidelineFeedback(storeRo, g2, u2, "Feedback from hq", [])
    addGuidelineFeedback(storeRo, g2, u5, "New Feedback from store", [i4])

    g3 = Guideline(name="Guideline 3", description="Description for Guideline 3", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g3, i7, [p1, p2, p3],[storeRo, storeNl], 3)
    company.guidelines.append(g3)
    addGuidelineFeedback(storeRo, g3, u5, "Image taken with the empty fixture", [i1])
    addGuidelineFeedback(storeRo, g3, u2, "Please send me back 3 more images with the fixture filled with products", [])
    addGuidelineFeedback(storeRo, g3, u5, "The requested images", [])
    addGuidelineFeedback(storeRo, g3, u5, "The requested images - sorry, in prev. message I forgot to attach the images", [i2,i4,i6])
    addGuidelineFeedback(storeRo, g3, u2, "Thanks, looking good!", [])

    g4 = Guideline(name="Guideline Mandatory Photo feedback", description="Description for Guideline Mandatory Photo feedback", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g4, i7, [p1, p2, p3], [storeRo, storeNl], 1)
    company.guidelines.append(g4)
    addGuidelineFeedback(storeRo, g4, u5, "Reply without photo", [])


    # save company
    sess.flush()
    sess.commit()


#Flask implentation
app = Flask(__name__)


class UserAPI(MethodView):

    def get(self):

        return jsonify(username="dan",
            email="dan.bunea@gmail.com",
            id=4)




#app.run()



#if __name__ == '__main__':
#    app.run(debug=True)

#webapp2 implemetation
#app = webapp2.WSGIApplication(
#	    [
#            ('/', MainHandler),
#            ('/guideline', SelectGuidelineHandler),
#            ('/dump', datadump.DumpHandler),
#	        ('/sign', GuestBook),
#            ('/inject',InjectorHandler)
#	    ],
#	    debug=True
#	)

	# wsgiref.handlers.CGIHandler().run(app)

# if __name__ == "__main__":
	# main()