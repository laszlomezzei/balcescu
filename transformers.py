from models import *


def convertDate(dateTime):
    return "2012-02-20";



class BaseTransformer(object):
    def to_json(self,obj):
        pass
    def from_json(self,obj):
        pass

    def to_json_list(self,list):
        mylist = []
        for el in list:
            mylist.append(self.to_json(el))
        return mylist



class GuidelineTransformer(BaseTransformer):
    def to_json(self, guideline):
        if isinstance(guideline,list):
            return self.to_json_list(guideline)

        #resp = 100 * guideline.getNumberOfStoresWithResponses() / guideline.getConversations().size()
        canvasTrans = Transformers.getInstance().canvasTransformer
        convTrans = Transformers.getInstance().guidelineConversationTransformer
        feedTrans = Transformers.getInstance().guidelineFeedbackTransformer
        return dict(id=guideline.id,
            description=guideline.description,
            due_date=convertDate(guideline.dueDate),
            name = guideline.name,
            number_of_stores_with_responses = 0, #resp
            photo_required = guideline.photoRequired,
            publication_date = convertDate(guideline.publicationDate),
            canvases = canvasTrans.to_json(guideline.canvases),
            #conversations = convTrans.to_json(guideline.guidelineconversations),
            #feedbacks = feedTrans.to_json(guideline.guidelinefeedbacks)
        )

class GuidelineFeedbackOverviewTransformer(BaseTransformer):
    def to_json(self,obj):
        if isinstance(obj,list):
            return self.to_json_list(obj);

        #resp = 100 * guideline.getNumberOfStoresWithResponses() / guideline.getConversations().size()
        convTrans = Transformers.getInstance().guidelineConversationTransformer
        return dict(guideline_id=obj.id,
            guideline_name=obj.name,
            guideline_due_date=convertDate(obj.dueDate),
            response_rate=0,
            conversations=convTrans.to_json(obj.guidelineconversations))

class GuidelineConversationTransformer(BaseTransformer):
    def to_json(self,conv):
        if isinstance(conv,list):
            return self.to_json_list(conv)

        return dict(guideline_id=conv.guideline.id,
            store_id=conv.store_id,
            store_name=conv.store.name,
            store_address=conv.store.address,
            message_count=conv.messageCount,
            unread=conv.unread,
            update_date=convertDate( conv.updateDate),
            images=Transformers.getInstance().imageTransformer.to_json(conv.thumbs)
        )

class GuidelineFeedbackTransformer(BaseTransformer):
    def to_json(self, gf):
        if isinstance(gf,list):
            return self.to_json_list(gf)

        return dict(id=gf.id,
            creation_date=convertDate(gf.creationDate),
            feedback=gf.feedback,
            guideline_id=gf.parent_id,
            store_id=gf.store_id,
            store_name=gf.store.name,
            store_address=gf.store.address,
            user_id=gf.user_id,
            user_roles = gf.user.roles,
            images =Transformers.getInstance().imageTransformer.to_json(gf.guidelinefeedbacksphotos),
            photo_keys = []
        )

class CanvasTransformer(BaseTransformer):
    def to_json(self, canvas):
        if isinstance(canvas,list):
            return self.to_json_list(canvas)

        hspotTrans = Transformers.getInstance().hotspotTransformer
        return dict(id=canvas.id,
            order=canvas.order,
            background_id=canvas.backgroundId,
            background_height = canvas.backgroundHeight,
            background_width = canvas.backgroundWidth,
            background_name = canvas.backgroundName,
            image_ratio = canvas.imageRatio,
            assets = hspotTrans.to_json(canvas.hotspots)
        )

    def from_json(self,json, canvas):
        hspotTrans = Transformers.getInstance().hotspotTransformer
        canvas.id=json['id']
        canvas.backgroundName=json['background_name']
        canvas.order=json['order']
        canvas.backgroundId=json['background_id']
        canvas.backgroundHeight = json['background_height']
        canvas.backgroundWidth = json['background_width']
        canvas.imageRatio = json['image_ratio']
        canvas.hotspots = hspotTrans.to_json(json['assets'])

class HotspotTransformer(BaseTransformer):

    def from_json(self,json, hotspot):

        #hotspot.id=json['id']
        # hotspot.imageRatio=json['image_ratio']
        hotspot.assetId=json['id']
        hotspot.order=json['order']
        hotspot.posx=json['posx']
        hotspot.posy=json['posy']
        hotspot.productImageName=json['image_name']
        hotspot.productName=json['name']
        hotspot.productNumber=json['product_number']
        hotspot.quantity=json['quantity']


    def to_json(self, hotspot):
        if isinstance(hotspot,list):
            return self.to_json_list(hotspot)

        return dict(id=hotspot.id,
            # image_ratio = hotspot.imageRatio,
            order=hotspot.order,
            posx = hotspot.posx,
            posy=hotspot.posy,
            product_image_name = hotspot.productImageName,
            product_name = hotspot.productName,
            product_number = hotspot.productNumber,
            quantity = hotspot.quantity
        )

class StoreTransformer(BaseTransformer):
    def to_json(self, store):
        if isinstance(store,list):
            return self.to_json_list(store)

        return dict(id=store.id,
            name=store.name,
            address=store.address
        )

class UserTransformer(BaseTransformer):
    def to_json(self, user):
        if isinstance(user,list):
            return self.to_json_list(user)

        return dict(id=user.id,
            email=user.email,
            password = user.password,
            roles = user.roles,
            store_id = user.store_id,
            username = user.username
        )

class AssetTransformer(BaseTransformer):
    def to_json(self, asset):
        if isinstance(asset,list):
            return self.to_json_list(asset)

        if asset.type == "Product":
            prodTrans = Transformers.getInstance().productTransformer
            return prodTrans.to_json(asset)
        else:
            fixtTrans = Transformers.getInstance().fixtureTransformer
            return fixtTrans.to_json(asset)

class ProductTransformer(BaseTransformer):
    def to_json(self, product):
        if isinstance(product,list):
            return self.to_json_list(product)

        tgroupsTrans = Transformers.getInstance().tagGroupTransformer
        return dict(id=product.id,
            creation_date = convertDate(product.creation_date),
            image_height = product.images[0].imageHeight,
            image_width = product.images[0].imageWidth,
            image_name = product.images[0].servingURL,
            #image_ratio = product.images[0].imageRatio,
            name=product.name,
            product_number = product.productId,
            type = product.type,
            #tag_groups = tgroupsTrans.to_json(product.taggroups)
        )

class FixtureTransformer(BaseTransformer):
    def to_json(self, fixture):
        if isinstance(fixture,list):
            return self.to_json_list(fixture)

        tgroupsTrans = Transformers.getInstance().tagGroupTransformer
        return dict(id=fixture.id,
            creation_date = convertDate( fixture.creation_date),
            image_height = fixture.images[0].imageHeight,
            image_width = fixture.images[0].imageWidth,
            image_name = fixture.images[0].servingURL,
            #image_ratio = fixture.images[0].ratio,
            name=fixture.name,
            product_number = fixture.fixtureId,
            type = fixture.type,
            #tag_groups = tgroupsTrans.to_json(fixture.taggroups)
        )

class TagGroupTransformer(BaseTransformer):
    def to_json(self, tgroup):
        if isinstance(tgroup,list):
            return self.to_json_list(tgroup)

        tagTrans = Transformers.getInstance().tagTransformer
        return dict(id=tgroup.id,
            mandatory_fixture = tgroup.mandatoryFixture,
            mandatory_product = tgroup.mandatoryProduct,
            name = tgroup.name,
            tags = tagTrans.to_json(tgroup.tags)
        )

class TagTransformer(BaseTransformer):
    def to_json(self, tag):
        if isinstance(tag,list):
            return self.to_json_list(tag)

        return dict(id=tag.id,
            name = tag.name
        )

class ManualGroupTransformer(BaseTransformer):
    def to_json(self, mgroup):
        if isinstance(mgroup,list):
            return self.to_json_list(mgroup)

        manualTrans = Transformers.getInstance().manualTransformer
        return dict(id=mgroup.id,
            name = mgroup.name,
            manuals = manualTrans.to_json(mgroup.manuals)
        )

class ManualTransformer(BaseTransformer):
    def to_json(self, manual):
        if isinstance(manual,list):
            return self.to_json_list(manual)

        return dict(id=manual.id,
            name = manual.name
        )


class ImageTransformer(BaseTransformer):
    def to_json(self, image):
        if isinstance(image,list):
            return self.to_json_list(image)

        return dict(
            url = image.servingURL,
            ratio = float(image.imageHeight)/image.imageWidth
        )

class Transformers:
    _instance=None

    def __init__(self):
        self.guidelineTransformer = GuidelineTransformer()
        self.guidelineFeedbackOverviewTransformer = GuidelineFeedbackOverviewTransformer()
        self.guidelineConversationTransformer=GuidelineConversationTransformer()
        self.guidelineFeedbackTransformer=GuidelineFeedbackTransformer()
        self.canvasTransformer=CanvasTransformer()
        self.hotspotTransformer=HotspotTransformer()
        self.storeTransformer=StoreTransformer()
        self.userTransformer=UserTransformer()
        self.assetTransformer=AssetTransformer()
        self.productTransformer=ProductTransformer()
        self.fixtureTransformer=FixtureTransformer()
        self.tagGroupTransformer=TagGroupTransformer()
        self.tagTransformer=TagTransformer()
        self.manualGroupTransformer=ManualGroupTransformer()
        self.manualTransformer=ManualTransformer()
        self.imageTransformer=ImageTransformer()


    def getInstance():
        if not Transformers._instance:
            Transformers._instance=Transformers()
        return Transformers._instance

    getInstance=staticmethod(getInstance)


