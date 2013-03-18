import os
import sys
from inject import injectData, injectDataMigration002, injectDataMigration003


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
        # Base.metadata.create_all(bind=migrate_engine)
        Session = sessionmaker(bind=migrate_engine)
        session = Session()
        f = open("migrations001.sql")
        script_str = f.read().strip()
        all_scripts = script_str.split(';')

        for sql in all_scripts:
            if(len(sql)>10):
                session.execute(sql)
                session.commit()

        injectData(Session())

        session.close()


    def down(self,migrate_engine):
        Base.metadata.drop_all(bind=migrate_engine)


class Migration002(VRBaseMigration):
    version = 2

    def up(self,migrate_engine):
        pass
        Session = sessionmaker(bind=migrate_engine)
        session = Session()
        f = open("migrations002.sql")
        script_str = f.read().strip()
        all_scripts = script_str.split(';')

        for sql in all_scripts:
            if(len(sql)>10):
                session.execute(sql)
                session.commit()

        injectDataMigration002(Session())

        session.close()
        # meta = MetaData(bind=migrate_engine)


        # storeGroupsTable = StoreGroup.__table__
        # storeGroupsTable.create()
        #
        # storesTable = Store.__table__
        # col = Column('store_group_id', Integer)
        # col.create(storesTable)
        #
        # usersTable = User.__table__
        # col = Column('storeGroup', Integer)
        # col.create(usersTable)

    def down(self,migrate_engine):
        pass



class Migration003(VRBaseMigration):
    version = 3

    def up(self,migrate_engine):
        pass
        Session = sessionmaker(bind=migrate_engine)
        session = Session()

        injectDataMigration003(Session())

        session.close()

    def down(self,migrate_engine):
        pass
