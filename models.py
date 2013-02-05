from google.appengine.ext import blobstore, db


class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class Company(DictModel):
	name = db.StringProperty(required=True)

class Store(db.Model):
	name = db.StringProperty(required=True)
	address=db.StringProperty(multiline=True)

class User(db.Model):
	email = db.StringProperty(required=True)
	username = db.StringProperty()
	password=db.StringProperty()
	roles=db.StringListProperty()
	store= db.ReferenceProperty(Store)

class Guideline(db.Model):
	name = db.StringProperty(required=True)
	search_name = db.StringProperty()
	description = db.StringProperty()
	search_description = db.StringProperty()
	dueDate = db.DateProperty()
	photoRequired = db.BooleanProperty(default = True)
	publicationDate = db.DateTimeProperty(auto_now_add=True)

class GuidelineConversation(db.Model):
	messageCount=db.IntegerProperty(default = 0)
	storeKey=db.ReferenceProperty(Store)
	unread = db.BooleanProperty(default = False)
	updateDate = db.DateTimeProperty()

class GuidelineFeedback(db.Model):
	creationDate = db.DateTimeProperty(auto_now_add=True)
	feedback = db.StringProperty()
	storeKey = db.ReferenceProperty(Store)
	userKey = db.ReferenceProperty(User)

class GuidelineFeedbackPhoto(db.Model):
	dashboardImageName = db.StringProperty()
	imageName = db.StringProperty()
	imageHeight = db.IntegerProperty()
	imageWidth = db.IntegerProperty()
	servingURL = db.StringProperty()

class GuidelineFeedbackPhotoThumb(db.Model):
	dashboardImageName = db.StringProperty()
	imageName = db.StringProperty()
	imageHeight = db.IntegerProperty()
	imageWidth = db.IntegerProperty()
	servingURL = db.StringProperty()

class Canvas(db.Model):
	backgroundName = db.StringProperty()
	backgroundId = db.IntegerProperty()
	backgroundHeight = db.IntegerProperty()
	backgroundWidth = db.IntegerProperty()
	imageRatio = db.FloatProperty()
	order = db.IntegerProperty()

class Hotspot(db.Model):
	id=db.IntegerProperty() #represents the productId, maybe should be renamed
	imageRatio = db.FloatProperty()
	order = db.IntegerProperty()
	posx = db.FloatProperty()
	posy=db.FloatProperty()
	productImageName = db.StringProperty()
	productName = db.StringProperty()
	search_productName = db.StringProperty()
	productNumber = db.StringProperty()
	search_productNumber = db.StringProperty()

class TagGroup(db.Model):
	name = db.StringProperty(required=True)
	search_name = db.StringProperty()
	mandatoryFixture  = db.BooleanProperty(default = False)
	mandatoryProduct  = db.BooleanProperty(default = False)

class Tag(db.Model):
	name = db.StringProperty(required=True)

class Image(db.Model):
	name = db.StringProperty(required=True)
	blob_key = blobstore.BlobReferenceProperty()
	imageWidth=db.IntegerProperty()
	imageHeight=db.IntegerProperty()
	servingURL=db.StringProperty(required=True)

class Fixture(db.Model):
	name = db.StringProperty(required=True)
	search_name=db.StringProperty()
	fixtureId=db.StringProperty()
	search_fixtureId=db.StringProperty()
	imageKey=db.StringProperty()
	creation_date=db.DateTimeProperty(auto_now_add=True);

class Product(db.Model):
	name = db.StringProperty(required=True)
	search_name=db.StringProperty()
	productId=db.StringProperty()
	search_productId=db.StringProperty()
	creation_date=db.DateTimeProperty(auto_now_add=True);
	imageKey=db.StringProperty()

class Device(db.Model):
	name = db.StringProperty(required=True)

class Company(db.Model):
	name = db.StringProperty(required=True)

class ManualGroup(db.Model):
	name = db.StringProperty(required=True)

class Manual(db.Model):
	name = db.StringProperty(required=True)



# A custom datastore model for associating users with uploaded files.
class UserPhoto(db.Model):
	user = db.StringProperty()
	blob_key = blobstore.BlobReferenceProperty()






