import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from models import *
from sqlalchemy import Table, MetaData, String, Column


class VRBaseMigration(object):
    version=0
    def up(self,engine):
        print "up"

    def down(self,engine):
        print "down"

    def fromJson(self):
        print "c"




class Migration001(VRBaseMigration):
    version = 1

    def up(self,migrate_engine):
        Base.metadata.create_all(bind=migrate_engine)


    def down(self,migrate_engine):
        Base.metadata.drop_all(bind=migrate_engine)


class Migration002(VRBaseMigration):
    version = 2

    def up(self,migrate_engine):
        meta = MetaData(bind=migrate_engine)

        #account = Table(Company.__tablename__, meta, autoload=True)
        #emailc = Column('email', String(128))
        #emailc.create(account)

        companiesTable = Table(Company.__tablename__,meta,autoload=True)
        companiesTable.append_column(Column('email', String(50)))
        #meta.

        meta.create_all(migrate_engine )




    def down(self,migrate_engine):
        meta = MetaData(bind=migrate_engine)
        companiesTable = Table(Company.__tablename__, meta, autoload=True)
        companiesTable.c.email.drop()