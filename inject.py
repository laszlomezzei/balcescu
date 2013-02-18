#from models import *
import main
from datetime import datetime, date, timedelta
from PIL import Image as PILImage
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import db

def addGuidelineFeedback(store, guideline, user, message, images):
    guidelinefeedback = main.GuidelineFeedback(feedback=message)
    user.guidelinefeedbacks.append(guidelinefeedback)
    store.guidelinefeedbacks.append(guidelinefeedback)
    guideline.guidelinefeedbacks.append(guidelinefeedback)

    for image in images:
        guidelinefeedback.guidelinefeedbacksphotos.append(main.GuidelineFeedbackPhoto(imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL))

	for conversation in guideline.guidelineconversations:
            if conversation.store_id == store.id:
                print "Update conversation for store: ", conversation.store_id
                contor = 1
                if isinstance(conversation.messageCount, int):
                    contor = conversation.messageCount + 1
                conversation.messageCount = contor
                conversation.unread = True
                conversation.updateDate = datetime.now()

                for image in images:
                    conversation.guidelinefeedbacksphotothumbs.append(main.GuidelineFeedbackPhotoThumb(imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL))



def addCanvasesAndHotspotsAndConversationsToGuideline(guideline, fixtureImage, products, stores, canvasCount):
    for cnvs in range(canvasCount):
        canvas = main.Canvas(backgroundName = fixtureImage.servingURL,
            backgroundId = fixtureImage.id,
            backgroundWidth=fixtureImage.imageWidth,
            backgroundHeight=fixtureImage.imageHeight,
            imageRatio=fixtureImage.imageHeight/float(fixtureImage.imageWidth),
            order = cnvs)

        i=0

        for product in products:
            image = product.images[0]
            hotspot = main.Hotspot(
                assetId = product.id,
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
            canvas.hotspots.append(hotspot)

            guideline.canvases.append(canvas)
        for store in stores:
            conversation = main.GuidelineConversation()
            store.guidelineconversations.append(conversation)
            guideline.guidelineconversations.append(conversation)



def uploadImage(filename):
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

	return main.Image(name=filename, imageWidth=im.size[0],imageHeight=im.size[1], servingURL=servingUrl)

