#from app import Session
from datetime import datetime, date, timedelta
from PIL import Image as PILImage
from google.appengine.api import files
from google.appengine.api import images
from database.models import *


def addGuidelineFeedback(store, guideline, user, message, images):
    guidelinefeedback = GuidelineFeedback(feedback=message)
    user.guidelinefeedbacks.append(guidelinefeedback)
    store.guidelinefeedbacks.append(guidelinefeedback)
    guideline.guidelinefeedbacks.append(guidelinefeedback)

    for image in images:
        guidelinefeedback.guidelinefeedbacksphotos.append(GuidelineFeedbackPhoto(imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL))

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
                    conversation.thumbs.append(GuidelineFeedbackPhotoThumb(imageName = image.name, imageWidth=image.imageWidth, imageHeight=image.imageHeight, servingURL=image.servingURL))



def addCanvasesAndHotspotsAndConversationsToGuideline(guideline, fixtureImage, products, stores, canvasCount):
    for cnvs in range(canvasCount):
        canvas = Canvas(backgroundName = fixtureImage.servingURL,
            backgroundId = fixtureImage.id,
            backgroundWidth=fixtureImage.imageWidth,
            backgroundHeight=fixtureImage.imageHeight,
            imageRatio=fixtureImage.imageHeight/float(fixtureImage.imageWidth),
            order = cnvs)

        i=0

        for product in products:
            image = product.images[0]
            hotspot = Hotspot(
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
        conversation = GuidelineConversation()
        store.guidelineconversations.append(conversation)
        guideline.guidelineconversations.append(conversation)



def uploadImage(filename):
	im = PILImage.open("database/images/"+filename)
	thumbnail = im.resize(im.size)
	#print im.format, im.size[0], im.mode, thumbnail.info

	file = open("database/images/"+filename)
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

	return Image(name=filename, imageWidth=im.size[0],imageHeight=im.size[1], servingURL=servingUrl)


def injectData(Session):
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
    sess = Session
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


def injectDataMigration002(Session):
    u1 = User(email="iss-acc-manager", username="Main account manager", password="1234", roles='["ROLE_USER", "ACCOUNT_ADMIN"]')
    # save company
    sess = Session
    sess.add(u1)
    sess.commit()
    companies = sess.query(Company).filter(Company.name=="VR").all()
    company=None
    if(len(companies)==1):
        company=companies[0]
    else:
        pass
    admin = User(email="admin", username="Administrator", password="1234", roles='["ROLE_USER", "ADMINISTRATOR"]')
    company.users.append(admin)

    europe = StoreGroup(name="Europe")
    europe_user = User(email="europe", username="Europe Region Manager", password="1234", roles='["ROLE_USER", "REGION_HQ"]')
    europe.users.append(europe_user)
    company.users.append(europe_user)

    stores  = sess.query(Store).all()
    for store in stores:
        store.storeGroup = europe
        manager = User(email=store.name.replace(" ","") + "_manager", username=store.name + " Manager", password="1234", roles='["ROLE_USER", "STORE_MANAGER"]')
        store.users.append(manager)
        company.users.append(manager)


    company.storegroups.append(europe)

    america = StoreGroup(name="North America")
    america_user = User(email="america", username="North America Region Manager", password="1234", roles='["ROLE_USER", "REGION_HQ"]')
    america.users.append(america_user)
    company.users.append(america_user)
    storeNA = Store(name="VR United States", address="Boston, 5th Avenue 2945")
    usa_manager = User(email="usa_manager", username="VR North America Store Manager", password="1234", roles='["ROLE_USER", "STORE_MANAGER"]')
    storeNA.users.append(usa_manager)
    company.users.append(usa_manager)
    usa_store = User(email="usa_store", username="VR North America Store", password="1234", roles='["ROLE_USER", "STORE"]')
    storeNA.users.append(usa_store)
    company.users.append(usa_store)
    company.stores.append(storeNA)

    company.storegroups.append(america)


    storeCH = Store(name="VR China", address="Shanghai, Tien An Men Square, 32")
    asia_manager = User(email="asia_manager", username="VR Asia Store Manager", password="1234", roles='["ROLE_USER", "STORE_MANAGER"]')
    storeCH.users.append(asia_manager)
    company.users.append(asia_manager)

    asia_store = User(email="asia_store", username="VR Asia Store", password="1234", roles='["ROLE_USER", "STORE"]')
    storeCH.users.append(asia_store)
    company.users.append(asia_store)

    company.stores.append(storeCH)

    dueDate = date.today()+timedelta(days=5)

    fixtures = sess.query(Fixture).all()
    fixtureImage = fixtures[0].images[0]
    products = sess.query(Product).all()

    g5 = Guideline(name="Guideline 5 - all over the world", description="Guideline 5 - all over the world", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g5, fixtureImage, [products[0], products[1], products[2]], company.stores, 1)
    company.guidelines.append(g5)
    addGuidelineFeedback(storeCH, g5, asia_store, "Reply without photo from Shenzen", [])


    g6 = Guideline(name="Guideline 6 - to all the world", description="Guideline 6 - to all the world", dueDate=dueDate)
    addCanvasesAndHotspotsAndConversationsToGuideline(g6, fixtureImage, [products[0], products[1], products[2]], company.stores, 1)
    company.guidelines.append(g6)
    addGuidelineFeedback(storeNA, g6, asia_store, "Reply without photo", [])

    # save company
    sess.flush()
    sess.commit()



def injectDataMigration003(Session):
    sess = Session
    companies = sess.query(Company).filter(Company.name=="VR").all()
    company=None
    if(len(companies)==1):
        company=companies[0]
    else:
        pass

    for x in range(1, 300):
        company.stores.append(Store(name="Big Company Store #"+str(x), address="Big Company Boulevard #"+str(x)))

    sess.flush()
    sess.commit()




def injectDataMigration004(Session):
    sess = Session

    # remove stores created at mig 003
    stores = sess.query(Store).filter(Store.name.like("Big Company Store%")).all()
    for store in stores:
        sess.delete(store)


    # create test company
    testcompany = Company(name = "Test write company")

    storeNl = Store(name="Test Store", address="Test store address")
    testcompany.stores.append(storeNl)

    # Create HQ Users
    u1 = User(email="test_write_hq", username="Test write company hq", password="1234", roles='["ROLE_USER", "HQ"]')
    # Create STORE Users
    u2 = User(email="test_write_store", username="test write company store", password="1234",roles='["ROLE_USER","STORE"]')

    testcompany.users=[u1,u2]

    storeNl.users=[u2]

    # Create Tag Group
    tg1 = TagGroup(name="Optional")
    tg2 = TagGroup(name="Brand", mandatoryProduct=True, tags=[Tag(name="Adidas"),Tag(name="Nike"),Tag(name="Puma")])
    testcompany.taggroups = [tg1, tg2]

    # upload images
    i7 = uploadImage("fixture1.png")
    i8 = uploadImage("product1.png")
    i9 = uploadImage("product2.png")
    i10 = uploadImage("product3.png")
    testcompany.images = [i7,i8,i9,i10]

    # Create fixtures
    f1 = Fixture(name="Fixture 1", search_name="fixture 1", fixtureId="1234", search_fixtureId="1234", images=[i7]) #
    testcompany.fixtures = [f1]

    # Create products
    p1 = Product(name="Product 1", productId="1", images=[i8])
    p2 = Product(name="Product 2", productId="2", images=[i9])
    p3 = Product(name="Product 3", productId="3", images=[i10])
    testcompany.products = [p1,p2,p3]

    sess.add(testcompany)

    # create new Big Company
    bigcompany = Company(name = "Big Company")
    sess.add(bigcompany)
    sess.commit()

    admin = User(email="big_admin", username="Administrator", password="1234", roles='["ROLE_USER", "ADMINISTRATOR"]')
    bigcompany.users.append(admin)

    for x in range(1, 301):
        store = Store(name="Big Company Store #"+str(x), address="Big Company Boulevard #"+str(x))
        store_user = User(email="big_store"+str(x), username="Big Company Store #"+str(x), password="1234", roles='["ROLE_USER", "STORE"]')
        store_manager = User(email="big_manager"+str(x), username="Big Company Manager #"+str(x), password="1234", roles='["ROLE_USER", "STORE_MANAGER"]')
        store.users.append(store_user)
        bigcompany.users.append(store_user)
        store.users.append(store_manager)
        bigcompany.users.append(store_manager)
        bigcompany.stores.append(store)





    sess.flush()
    sess.commit()