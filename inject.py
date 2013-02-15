#from models import *
from main import *
from datetime import datetime, date, timedelta
from PIL import Image as PILImage
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import db

def addGuidelineFeedback(company_key, store, guideline, user, message, images):
	feedback = GuidelineFeedback(parent = guideline.key(), storeKey=store, userKey=user, feedback=message)
	feedback.put()
	for image in images:
		gfp = GuidelineFeedbackPhoto(parent = feedback.key(), imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL)
		gfp.put()
	q = GuidelineConversation.all()
	conversations = q.filter('storeKey =', store.key()).ancestor(guideline.key()).run()
	#print conversations
	for conversation in conversations:
		conversation.messageCount=conversation.messageCount+1
		conversation.unread = True
		conversation.updateDate = datetime.now()
		conversation.put()
		for image in images:
			gfpt = GuidelineFeedbackPhotoThumb(parent = conversation.key(), imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL)
			gfpt.put()
		


def addCanvasesAndHotspotsAndConversationsToGuideline(company_key, stores, guideline, fixtureImage, products, canvasCount):
	for cnvs in range(canvasCount):
		canvas = Canvas(backgroundName = fixtureImage.servingURL, 
			backgroundId = fixtureImage.key().id(), 
			backgroundWidth=fixtureImage.imageWidth, 
			backgroundHeight=fixtureImage.imageHeight, 
			imageRatio=fixtureImage.imageHeight/float(fixtureImage.imageWidth), 
			order = cnvs)
		canvas.put()
		i=0
		for product in products:
			image = db.get(product.imageKey)
			hotspot = Hotspot(parent=company_key,
				id=product.key().id(),
				imageRatio = image.imageHeight/float(image.imageWidth),
				order=i,
				posx=(10+i)*float(i+1),
				posy=(15+i)*float(i+1),
				productImageName=image.servingURL,
				productName=product.name,
				productNumber=product.productId,
				quantity=8,
				search_productName=product.search_name,
				search_productNumber=product.search_productId)
			i=i+1
			hotspot.put()
	for store in stores:
		gc = GuidelineConversation(parent = guideline.key(), storeKey=store)
		gc.put()


def uploadImage(company_key, filename):
	im = PILImage.open("images/"+filename)
	thumbnail = im.resize(im.size)
	#print im.format, im.size[0], im.mode, thumbnail.info

	file = open("images/"+filename)
	data = file.read()
	file.close()

	# Create the file
	file_name = files.blobstore.create(mime_type = "image/png",_blobinfo_uploaded_filename=filename)

	# Open the file and write to it
	with files.open(file_name, 'a') as f:
		f.write(data)

	# Finalize the file. Do this before attempting to read it.
	files.finalize(file_name)

	# Get the file's blob key
	blob_key = files.blobstore.get_blob_key(file_name)
	servingUrl = images.get_serving_url(blob_key)
	return Image(parent=company_key, name=filename, blob_key=blob_key, imageWidth=im.size[0],imageHeight=im.size[1], servingURL=servingUrl)

