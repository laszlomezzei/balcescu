import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, inspect, create_engine, Table, Float
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from datetime import datetime, date, timedelta



class VRBase(object):
    def doit(self):
        print "a"

    def toJson(self):
        print "b"

    def fromJson(self):
        print "c"

Base = declarative_base(cls=VRBase)
#Base.query = db_session.query_property()


class DatabaseSchema(Base):
    __tablename__ = 'DatabaseSchema'
    id = Column(Integer, primary_key=True)
    version = Column(Integer)

    def __init__(self, version):
        self.version = version

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
    users=relationship("User", backref="store")
    devices=relationship("Device", backref="store")
    # store_group_id = Column(Integer, ForeignKey('StoreGroups.id'))
    guidelineconversations=relationship("GuidelineConversation", backref="store")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="store")

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), default='')
    username = Column(String(255), default='')
    password = Column(String(255), default='')
    roles = Column(String(255), default='')
    parent_id = Column(Integer, ForeignKey('Companies.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="user")
    storeGroup = relationship("StoreGroup", uselist=False, backref="user")

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
    creation_date=Column(DateTime, default=datetime.now()) # auto_now_add=True
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
    canvases=relationship("Canvas", backref="guideline")
    guidelineconversations=relationship("GuidelineConversation", backref="guideline")
    guidelinefeedbacks=relationship("GuidelineFeedback", backref="guideline")



class GuidelineConversation(Base):
    __tablename__ = 'GuidelineConversations'
    id = Column(Integer, primary_key=True)
    messageCount=Column(Integer, default=0)
    unread = Column(Boolean, default = False)
    updateDate = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('Guidelines.id'))
    store_id = Column(Integer, ForeignKey('Stores.id'))
    thumbs=relationship("GuidelineFeedbackPhotoThumb", backref="guidelineConversation")

class GuidelineFeedback(Base):
    __tablename__ = 'GuidelineFeedbacks'
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime,default=datetime.now())
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
    hotspots=relationship("Hotspot", backref="canvas")


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


class StoreGroup(Base):
    __tablename__ = 'StoreGroups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    isArchived = Column(Boolean, default = False)
    # stores=relationship("Store", backref="storeGroup")
    user_id = Column(Integer, ForeignKey('Users.id'))