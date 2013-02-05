#!/usr/bin/env python

import wsgiref.handlers
import json

from inject import *
from models import *


from datetime import datetime, date, timedelta

from PIL import Image as PILImage
from google.appengine.api import users
from google.appengine.api import files
from google.appengine.api import images

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app











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


class InjectorHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'

		company  = Company(name="VR")
		company.put()

		notExitingStore = Store(name="not existing")
		storeRo = Store(parent=company.key(), name="VR Romania", address="Pta Balcescu 4/6, Timisoara")
		storeNl = Store(parent=company.key(), name="VR Nederland", address="Ruyterkade 6, Amsterdam")
		storeRo.put()
		storeNl.put()
		
		# Create HQ Users 
		u1 = User(parent=company.key(), email="marten", username="Marten HQ", password="1234", roles=["ROLE_USER", "HQ"])
		u2 = User(parent=company.key(), email="dan", username="Dan HQ", password="1234",roles=["ROLE_USER","HQ"]);
		u3 = User(parent=company.key(), email="laci", username="Laszlo HQ", password="1234",roles=["ROLE_USER","HQ"]);
    	# Create STORE Users
		u4 = User(parent=company.key(), store=storeNl, email="marten_store", username="Marten Store", password="1234",roles=["ROLE_USER","STORE"]);
		u5 = User(parent=company.key(), store=storeNl, email="dan_store", username="Dan Store", password="1234",roles=["ROLE_USER","STORE"]);
		u6 = User(parent=company.key(), store=storeNl, email="laci_store", username="Laszlo Store", password="1234",roles=["ROLE_USER","STORE"]);

		db.put([u1, u2, u3, u4, u5, u6])

		# Create Tag Group
		tg1 = TagGroup(parent = company.key(), name="Optional")
		tg1.put()

		#upload images
		i1 = uploadImage(company.key(), "img1.png")
		i2 = uploadImage(company.key(), "dashboard_dummy_thumb_1.png")
		i3 = uploadImage(company.key(), "dashboard_dummy_thumb_2.png")
		i4 = uploadImage(company.key(), "dashboard_dummy_thumb_3.png")
		i5 = uploadImage(company.key(), "dashboard_dummy_thumb_4.png")
		i6 = uploadImage(company.key(), "dashboard_dummy_thumb_5.png")
		i7 = uploadImage(company.key(), "fixture1.png")
		i8 = uploadImage(company.key(), "product1.png")
		i9 = uploadImage(company.key(), "product2.png")
		i10 = uploadImage(company.key(), "product3.png")
		db.put([i1,i2,i3,i4,i5,i6,i7,i8,i9,i10])

		# Create fixtures
		f1 = Fixture(parent=company.key(), name="Fixture 1", search_name="fixture 1", fixtureId="1234", search_fixtureId="1234", imageKey=str(i7.key()))
		f1.put()

		# Create products
		p1 = Product(parent=company.key(), name="Product 1", search_name="product 1", productId="Prod 1111", search_productId="prod 1111", imageKey=str(i8.key()))
		p2 = Product(parent=company.key(), name="Product 2", search_name="product 2", productId="Prod 1112", search_productId="prod 1112", imageKey=str(i9.key()))
		p3 = Product(parent=company.key(), name="Product 3", search_name="product 3", productId="Prod3", search_productId="prod3", imageKey=str(i10.key()))
		db.put([p1,p2,p3])
		
		# Create guidelines and feedbacks
		
		dueDate = date.today()+timedelta(days=5)

		g1 = Guideline(parent=company.key(), name="Guideline 1", search_name="guideline 1", description="Description for Guideline 1", search_description="description for guideline 1", dueDate=dueDate)
		db.put(g1)
		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g1, i7, [p1,p2], 1)
		addGuidelineFeedback(company.key(), storeRo, g1, u6, "Feedback from store", [i2])
		addGuidelineFeedback(company.key(), storeNl, g1, u4, "Feedback from store", [i6])

		g2 = Guideline(parent=company.key(), name="Guideline 2", search_name="guideline 2", description="Description for Guideline 2", search_description="description for guideline 2", dueDate=dueDate)
		db.put(g2)
		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g2, i7, [p1], 1)
		addGuidelineFeedback(company.key(), storeRo, g2, u5, "Feedback from store", [i3])
		addGuidelineFeedback(company.key(), storeRo, g2, u2, "Feedback from hq", [])
		addGuidelineFeedback(company.key(), storeRo, g2, u5, "New Feedback from store", [i4])

		g3 = Guideline(parent=company.key(), name="Guideline 3", search_name="guideline 3", description="Description for Guideline 3", search_description="description for guideline 3", dueDate=dueDate)
		db.put(g3)
		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g3, i7, [p1, p2, p3], 3)
		addGuidelineFeedback(company.key(), storeRo, g3, u5, "Image taken with the empty fixture", [i1])
		addGuidelineFeedback(company.key(), storeRo, g3, u2, "Please send me back 3 more images with the fixture filled with products", [])
		addGuidelineFeedback(company.key(), storeRo, g3, u5, "The requested images", [])
		addGuidelineFeedback(company.key(), storeRo, g3, u5, "The requested images - sorry, in prev. message I forgot to attach the images", [i2,i4,i6])
		addGuidelineFeedback(company.key(), storeRo, g3, u2, "Thanks, looking good!", [])
		

		g4 = Guideline(parent=company.key(), name="Guideline Mandatory Photo feedback", search_name="Guideline Mandatory Photo feedback", description="Description for Guideline Mandatory Photo feedback", search_description="description for Guideline Mandatory Photo feedback", dueDate=dueDate)
		db.put(g4)
		addCanvasesAndHotspotsAndConversationsToGuideline(company.key(), [storeRo, storeNl], g4, i7, [p1, p2, p3], 1)
		addGuidelineFeedback(company.key(), storeRo, g4, u5, "Reply without photo", [])

		json.dump({"name":company.name},self.response.out)




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

def main():
	app=webapp.WSGIApplication([
		('/',MyHandler),
		('/inject',InjectorHandler),
		('/upload_form', PhotoUploadFormHandler),	
        ('/upload_photo', PhotoUploadHandler),
        ('/view_photo/([^/]+)?', ViewPhotoHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)

def to_json(obj):
    return dict([(p, unicode(getattr(obj, p))) for p in obj.properties()])

if __name__ == "__main__":
	main()