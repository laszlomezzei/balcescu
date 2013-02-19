#!/usr/bin/env python

# import wsgiref.handlers
# import json

# from inject import *
# from models import *
# from gqlencoder import encode

# from datetime import datetime, date, timedelta

# from PIL import Image as PILImage
# from google.appengine.api import users
# from google.appengine.api import files
# from google.appengine.api import images

# from google.appengine.ext import blobstore
# from google.appengine.ext import db
# from google.appengine.ext import webapp
# from google.appengine.ext.webapp import blobstore_handlers
# from google.appengine.ext.webapp.util import run_wsgi_app

# standard libraries
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, inspect, create_engine, Table, Float
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


# App Engine libraries
import jinja2
import json
import webapp2
import datadump
from inject import *
from google.appengine.api import rdbms
#import sqlalchemy
#from sqlalchemy import *
#from sqlalchemy.orm import *
#from sqlalchemy.inspection import *
#from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


#import MySQLdb
#
#db = MySQLdb.connect(host="localhost", # your host, usually localhost
#    user="root", # your username
#    passwd="", # your password
#    db="shopshape") # name of the data base
#
## you must create a Cursor object. It will let
##  you execute all the query you need
#cur = db.cursor()
#
## Use all the SQL you like
#cur.execute("SELECT * FROM table1")
#
## print all the first cell of all the rows
#for row in cur.fetchall() :
#    print row[0]


## App specific libraries
import settings

class GetConnection():
    """A guard class for ensuring the connection will be closed."""

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = rdbms.connect(instance=settings.CLOUDSQL_INSTANCE,
                                  database=settings.DATABASE_NAME, user=settings.USER_NAME, password=settings.PASSWORD)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()


jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__))))



#engine = create_engine('sqlite:///tutorial.db')
engine = create_engine('mysql+mysqldb://root@localhost/'+settings.DATABASE_NAME, echo=True)
db_session = scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)






class MainHandler(webapp2.RequestHandler):

    def get(self):
        init_db()

class VRBase(object):
    def doit(self):
        print "a"

    def toJson(self):
        print "b"

    def fromJson(self):
        print "c"

Base = declarative_base(cls=VRBase)
Base.query = db_session.query_property()

class Company(Base):
    __tablename__ = 'Companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    stores = relationship("Store", backref="Companies")
    users = relationship("User", backref="Companies")
    manualgroups=relationship("ManualGroup", backref="Companies")
    taggroups=relationship("TagGroup", backref="Companies")
    images=relationship("Image", backref="Companies")
    fixtures=relationship("Fixture", backref="Companies")
    products=relationship("Product", backref="Companies")
    devices=relationship("Device", backref="Companies")
    guidelines=relationship("Guideline", backref="Companies")

    def __init__(self, name):
        self.name = name


class Store(Base):
    __tablename__ = 'Stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    address = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    users=relationship("User", backref="Store")
    devices=relationship("Device", backref="Store")
    guidelineconversations=relationship("GuidelineConversation", backref="Store")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="Store")

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), default='')
    username = Column(String(255), default='')
    password = Column(String(255), default='')
    roles = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="Users")

class ManualGroup(Base):
    __tablename__ = 'ManualGroups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    manuals=relationship("Manual", backref="ManualGroups")

class Manual(Base):
    __tablename__ = 'Manuals'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('ManualGroups.id'))

class TagGroup(Base):
    __tablename__ = 'TagGroups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    search_name = Column(String(255), default='')
    mandatoryFixture  = Column(Boolean ,default = False)
    mandatoryProduct  = Column(Boolean ,default = False)
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    tags=relationship("Tag", backref="TagGroups")

class Tag(Base):
    __tablename__ = 'Tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('TagGroups.id'))

class Image(Base):
    __tablename__ = 'Images'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    #blob_key = blobstore.BlobReferenceProperty()
    imageWidth = Column(Integer, default='0')
    imageHeight = Column(Integer, default='0')
    servingURL=Column(String(255))
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    asset_id = Column(Integer, ForeignKey('Assets.id'))

class Asset(Base):
    __tablename__ = "Assets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    search_name = Column(String(255), default='')
    creation_date=Column(DateTime, default=datetime.now) # auto_now_add=True
    images = relationship("Image", backref="Asset")
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'Assets',
        'polymorphic_on':type
    }

association_tagstofixtures = Table('AssociationTagsToFixture', Base.metadata,
    Column('tag_id', Integer, ForeignKey('Tags.id')),
    Column('fixture_id', Integer, ForeignKey('Fixtures.id'))
)

class Fixture(Asset):
    __tablename__ = 'Fixtures'
    id = Column(Integer, ForeignKey('Assets.id'), primary_key=True)
    fixtureId = Column(String(255), default='')
    search_fixtureId = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    tags = relationship("Tag", secondary=association_tagstofixtures, backref="fixtures")

    __mapper_args__ = {
        'polymorphic_identity':'Fixtures'
    }

association_tagstoproducts = Table('AssociationTagsToProducts', Base.metadata,
    Column('tag_id', Integer, ForeignKey('Tags.id')),
    Column('product_id', Integer, ForeignKey('Products.id'))
)

class Product(Asset):
    __tablename__ = 'Products'
    id = Column(Integer, ForeignKey('Assets.id'), primary_key=True)
    productId = Column(String(255), default='')
    search_productId = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    tags = relationship("Tag", secondary=association_tagstoproducts, backref="products")

    __mapper_args__ = {
        'polymorphic_identity':'Products'
    }
class Device(Base):
    __tablename__ = 'Devices'
    id = Column(Integer, primary_key=True)
    deviceId = Column(String(255), default='')
    tokenId = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))

class Guideline(Base):
    __tablename__ = 'Guidelines'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    search_name = Column(String(255), default='')
    description = Column(String(255), default='')
    search_description = Column(String(255), default='')
    dueDate = Column(DateTime)
    photoRequired = Column(Boolean, default=True)
    publicationDate = Column(DateTime, default=datetime.now())
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    canvases=relationship("Canvas", backref="Guidelines")
    guidelineconversations=relationship("GuidelineConversation", backref="Guidelines")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="Guidelines")

    def toJson(self):
        return as_dict(self)

class GuidelineConversation(Base):
    __tablename__ = 'GuidelineConversations'
    id = Column(Integer, primary_key=True)
    messageCount=Column(Integer, default=0)
    unread = Column(Boolean, default = False)
    updateDate = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('Guidelines.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    guidelinefeedbacksphotothumbs=relationship("GuidelineFeedbackPhotoThumb", backref="GuidelineConversations")

class GuidelineFeedback(Base):
    __tablename__ = 'GuidelineFeedbacks'
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime,default=datetime.now)
    feedback = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Guidelines.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    guidelinefeedbacksphotos=relationship("GuidelineFeedbackPhoto", backref="GuidelineFeedback")

class GuidelineFeedbackPhoto(Base):
    __tablename__ = 'GuidelineFeedbackPhotos'
    id = Column(Integer, primary_key=True)
    dashboardImageName = Column(String(255), default='')
    imageName = Column(Integer)
    imageHeight = Column(Integer)
    imageWidth =Column(Integer)
    servingURL = Column(String(255))
    parent_id = Column(Integer, ForeignKey('GuidelineFeedbacks.id'))

class GuidelineFeedbackPhotoThumb(Base):
    __tablename__ = 'GuidelineFeedbackPhotoThumbs'
    id = Column(Integer, primary_key=True)
    dashboardImageName = Column(String(255))
    imageName = Column(String(255))
    imageHeight = Column(Integer)
    imageWidth =Column(Integer)
    servingURL = Column(String(255))
    parent_id = Column(Integer, ForeignKey('GuidelineConversations.id'))

class Canvas(Base):
    __tablename__ = 'Canvases'
    id = Column(Integer, primary_key=True)
    backgroundName = Column(String(255), default='')
    backgroundId = Column(Integer)
    backgroundHeight = Column(Integer)
    backgroundWidth = Column(Integer)
    imageRatio = Column(Float)
    order = Column(Integer)
    parent_id = Column(Integer, ForeignKey('Guidelines.id'))
    hotspots=relationship("Hotspot", backref="Canvases")


class Hotspot(Base):
    __tablename__ = 'Hotspots'
    id = Column(Integer, primary_key=True)
    assetId=Column(Integer) #oldname: id - represents the productId, maybe should be renamed
    imageRatio = Column(Float)
    order = Column(Integer)
    posx = Column(Float)
    posy=Column(Float)
    quantity = Column(Integer)
    productImageName = Column(String(255))
    productName = Column(String(255))
    search_productName = Column(String(255))
    productNumber = Column(String(255))
    search_productNumber = Column(String(255))
    parent_id = Column(Integer, ForeignKey('Canvases.id'))


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
        guidelines = select()
#        print guidelines
#        jsonx=json.dumps({"results":guidelines[0]}, cls=new_alchemy_encoder(False, ['guidelineconversations', 'Store']), check_circular=False  )
        #print jsonx
        #json.dump(jsonx, self.response.out)
        self.response.out.write(guidelines[0].toJson())





def select():
    session = Session()
    gl = session.query(Guideline).options(joinedload(Guideline.guidelineconversations, GuidelineConversation.Store))
    session.close()
    return gl.all()

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





app = webapp2.WSGIApplication(
	    [
            ('/', MainHandler),
            ('/guideline', SelectGuidelineHandler)
#            ('/dump', datadump.DumpHandler),
#	        ('/sign', GuestBook),
#            ('/inject',InjectorHandler)
	    ],
	    debug=True
	)

	# wsgiref.handlers.CGIHandler().run(app)

# if __name__ == "__main__":
	# main()