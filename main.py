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

# App Engine libraries
import jinja2
import json
import webapp2
import datadump
from inject import *
from google.appengine.api import rdbms
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


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






class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Viewing guestbook

        init_db()
        """
        print "MainHandler"
        with GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM table1')
            rows = cursor.fetchall()
        template_values = {'rows': rows}
        template = jinja2_env.get_template('index.html')
        kinds = datadump.get_kinds()
        print kinds
        self.response.out.write(template.render(template_values))
        """

#class GuestBook(webapp2.RequestHandler):
#
#    def post(self):
#        # Posting a new guestbook entry
#        print "GuestBook"
#        with GetConnection() as conn:
#            cursor = conn.cursor()
#            cursor.execute('INSERT INTO entries (guest_name, content) '
#                           'VALUES (%s, %s)',
#                           (self.request.get('guest_name'),
#                            self.request.get('content')))
#            conn.commit()
#        self.redirect('/')

#engine = create_engine('sqlite:///tutorial.db')
engine = create_engine('mysql+mysqldb://root@localhost/'+settings.DATABASE_NAME, echo=True)
db_session = scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(bind=engine)
Base = declarative_base()
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
    users=relationship("User", backref="Stores")
    devices=relationship("Device", backref="Stores")
    guidelineconversations=relationship("GuidelineConversation", backref="Stores")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="Stores")

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

association_tagstofixtures = Table('AssociationTagsToFixture', Base.metadata,
    Column('tag_id', Integer, ForeignKey('Tags.id')),
    Column('fixture_id', Integer, ForeignKey('Fixtures.id'))
)

class Fixture(Base):
    __tablename__ = 'Fixtures'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    search_name = Column(String(255), default='')
    fixtureId = Column(String(255), default='')
    search_fixtureId = Column(String(255), default='')
    #imageKey=db.StringProperty()
    creation_date=Column(DateTime) # auto_now_add=True
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    tags = relationship("Tag", secondary=association_tagstofixtures, backref="fixtures")

association_tagstoproducts = Table('AssociationTagsToProducts', Base.metadata,
    Column('tag_id', Integer, ForeignKey('Tags.id')),
    Column('product_id', Integer, ForeignKey('Products.id'))
)

class Product(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    search_name = Column(String(255), default='')
    productId = Column(String(255), default='')
    search_productId = Column(String(255), default='')
    #imageKey=db.StringProperty()
    creation_date=Column(DateTime) # auto_now_add=True
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    tags = relationship("Tag", secondary=association_tagstoproducts, backref="products")

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
    publicationDate = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    canvases=relationship("Canvas", backref="Guidelines")
    guidelineconversations=relationship("GuidelineConversation", backref="Guidelines")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="Guidelines")

class GuidelineConversation(Base):
    __tablename__ = 'GuidelineConversations'
    id = Column(Integer, primary_key=True)
    messageCount=Column(Integer, default='0')
    #storeKey=db.ReferenceProperty(Store)
    unread = Column(Boolean, default = False)
    updateDate = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('Guidelines.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    guidelinefeedbacksphotothumbs=relationship("GuidelineFeedbackPhotoThumb", backref="GuidelineConversations")

class GuidelineFeedback(Base):
    __tablename__ = 'GuidelineFeedbacks'
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime)
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
    productImageName = Column(String(255))
    productName = Column(String(255))
    search_productName = Column(String(255))
    productNumber = Column(String(255))
    search_productNumber = Column(String(255))
    parent_id = Column(Integer, ForeignKey('Canvases.id'))








def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


"""

class Products(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		products = db.GqlQuery('SELECT * FROM Product')
		self.response.out.write(encode(products))




class MyHandler(webapp.RequestHandler):
	def get(self):
		company=Company(
			name=self.request.get('name'))
		company.put()

		companies = db.GqlQuery(
			'SELECT * FROM Company')
		values={
			'companies':companies
		}
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write("company saved")
"""
#init_db()

class InjectorHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
        sess = Session()
        company = Company(name = "VR")
        print "Company name: ", company.name
        sess.add(company)
        sess.flush()
        sess.commit()
        #
        #		company = Company(name = "VR")
        #        print company.name
        #		db_session.add(company)
        #        db_session.commit()
        #        json.dump({"name":company.name},self.response.out)

        #		notExitingStore = Store(name="not existing")
        #		storeRo = Store(parent=company.key(), name="VR Romania", address="Pta Balcescu 4/6, Timisoara")
        #		storeNl = Store(parent=company.key(), name="VR Nederland", address="Ruyterkade 6, Amsterdam")
        #		storeRo.put()
        #		storeNl.put()
		
		# Create HQ Users 
        #		u1 = User(parent=company.key(), email="marten", username="Marten HQ", password="1234", roles=["ROLE_USER", "HQ"])
        #		u2 = User(parent=company.key(), email="dan", username="Dan HQ", password="1234",roles=["ROLE_USER","HQ"]);
        #		u3 = User(parent=company.key(), email="laci", username="Laszlo HQ", password="1234",roles=["ROLE_USER","HQ"]);
        #    	# Create STORE Users
        #		u4 = User(parent=company.key(), store=storeNl, email="marten_store", username="Marten Store", password="1234",roles=["ROLE_USER","STORE"]);
        #		u5 = User(parent=company.key(), store=storeNl, email="dan_store", username="Dan Store", password="1234",roles=["ROLE_USER","STORE"]);
        #		u6 = User(parent=company.key(), store=storeNl, email="laci_store", username="Laszlo Store", password="1234",roles=["ROLE_USER","STORE"]);
        #
        #		db.put([u1, u2, u3, u4, u5, u6])
        #
        #		# Create Tag Group
        #		tg1 = TagGroup(parent = company.key(), name="Optional")
        #		tg1.put()
        #
        #		#upload images
        #		i1 = uploadImage(company.key(), "img1.png")
        #		i2 = uploadImage(company.key(), "dashboard_dummy_thumb_1.png")
        #		i3 = uploadImage(company.key(), "dashboard_dummy_thumb_2.png")
        #		i4 = uploadImage(company.key(), "dashboard_dummy_thumb_3.png")
        #		i5 = uploadImage(company.key(), "dashboard_dummy_thumb_4.png")
        #		i6 = uploadImage(company.key(), "dashboard_dummy_thumb_5.png")
        #		i7 = uploadImage(company.key(), "fixture1.png")
        #		i8 = uploadImage(company.key(), "product1.png")
        #		i9 = uploadImage(company.key(), "product2.png")
        #		i10 = uploadImage(company.key(), "product3.png")
        #		db.put([i1,i2,i3,i4,i5,i6,i7,i8,i9,i10])
        #
        #		# Create fixtures
        #		f1 = Fixture(parent=company.key(), name="Fixture 1", search_name="fixture 1", fixtureId="1234", search_fixtureId="1234", imageKey=str(i7.key()))
        #		f1.put()
        #
        #		# Create products
        #		p1 = Product(parent=company.key(), name="Product 1", productId="1", imageKey=str(i8.key()))
        #		p2 = Product(parent=company.key(), name="Product 2", productId="2", imageKey=str(i9.key()))
        #		p3 = Product(parent=company.key(), name="Product 3", productId="3", imageKey=str(i10.key()))
        #		db.put([p1,p2,p3])
        #
        #		# Create guidelines and feedbacks
        #
        #		dueDate = date.today()+timedelta(days=5)
        #
        #		g1 = Guideline(parent=company.key(), name="Guideline 1", description="Description for Guideline 1", dueDate=dueDate)
        #		db.put(g1)
        #		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g1, i7, [p1,p2], 1)
        #		addGuidelineFeedback(company.key(), storeRo, g1, u6, "Feedback from store", [i2])
        #		addGuidelineFeedback(company.key(), storeNl, g1, u4, "Feedback from store", [i6])
        #
        #		g2 = Guideline(parent=company.key(), name="Guideline 2", description="Description for Guideline 2", dueDate=dueDate)
        #		db.put(g2)
        #		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g2, i7, [p1], 1)
        #		addGuidelineFeedback(company.key(), storeRo, g2, u5, "Feedback from store", [i3])
        #		addGuidelineFeedback(company.key(), storeRo, g2, u2, "Feedback from hq", [])
        #		addGuidelineFeedback(company.key(), storeRo, g2, u5, "New Feedback from store", [i4])
        #
        #		g3 = Guideline(parent=company.key(), name="Guideline 3", description="Description for Guideline 3", dueDate=dueDate)
        #		db.put(g3)
        #		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g3, i7, [p1, p2, p3], 3)
        #		addGuidelineFeedback(company.key(), storeRo, g3, u5, "Image taken with the empty fixture", [i1])
        #		addGuidelineFeedback(company.key(), storeRo, g3, u2, "Please send me back 3 more images with the fixture filled with products", [])
        #		addGuidelineFeedback(company.key(), storeRo, g3, u5, "The requested images", [])
        #		addGuidelineFeedback(company.key(), storeRo, g3, u5, "The requested images - sorry, in prev. message I forgot to attach the images", [i2,i4,i6])
        #		addGuidelineFeedback(company.key(), storeRo, g3, u2, "Thanks, looking good!", [])
        #
        #
        #		g4 = Guideline(parent=company.key(), name="Guideline Mandatory Photo feedback", description="Description for Guideline Mandatory Photo feedback", dueDate=dueDate)
        #		db.put(g4)
        #		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g4, i7, [p1, p2, p3], 1)
        #		addGuidelineFeedback(company.key(), storeRo, g4, u5, "Reply without photo", [])
        #



"""
class PhotoUploadFormHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_photo')
        # The method must be "POST" and enctype must be set to "multipart/form-data".
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write('''Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>''')

class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            user_photo = UserPhoto(user="Dan",
                                   blob_key=upload.key())
            db.put(user_photo)

            self.redirect('/view_photo/%s' % upload.key())

        except:
            self.redirect('/upload_failure.html')

class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
"""

# def main():
app = webapp2.WSGIApplication(
	    [
            ('/', MainHandler),
            ('/dump', datadump.DumpHandler),
#	        ('/sign', GuestBook),
            ('/inject',InjectorHandler)
	    ],
	    debug=True
	)
	# app=webapp.WSGIApplication([
	# 	('/',MyHandler),
	# 	('/inject',InjectorHandler),
	# 	('/upload_form', PhotoUploadFormHandler),	
 #        ('/upload_photo', PhotoUploadHandler),
 #        ('/service/product/all', Products),
 #        ('/view_photo/([^/]+)?', ViewPhotoHandler)], debug=True)
	# wsgiref.handlers.CGIHandler().run(app)

# def to_json(obj):
#     return dict([(p, unicode(getattr(obj, p))) for p in obj.properties()])

# if __name__ == "__main__":
	# main()