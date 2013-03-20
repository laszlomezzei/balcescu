import os
import sys
from database.inject import injectData, injectDataMigration002, injectDataMigration003, injectDataMigration004


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from database.models import *


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
        Session = sessionmaker(bind=migrate_engine)
        session = Session()
        f = open("database/migrations001.sql")
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
        Session = sessionmaker(bind=migrate_engine)
        session = Session()
        f = open("database/migrations002.sql")
        script_str = f.read().strip()
        all_scripts = script_str.split(';')

        for sql in all_scripts:
            if(len(sql)>10):
                session.execute(sql)
                session.commit()

        injectDataMigration002(Session())

        session.close()


    def down(self,migrate_engine):
        pass



class Migration003(VRBaseMigration):
    version = 3

    def up(self,migrate_engine):
        Session = sessionmaker(bind=migrate_engine)
        session = Session()

        injectDataMigration003(Session())

        session.close()

    def down(self,migrate_engine):
        pass




class Migration004(VRBaseMigration):
    version = 4

    def up(self,migrate_engine):
        Session = sessionmaker(bind=migrate_engine)
        session = Session()
        f = open("database/migrations004.sql")
        script_str = f.read().strip()
        all_scripts = script_str.split(';')

        for sql in all_scripts:
            if(len(sql)>10):
                session.execute(sql)
                session.commit()

        injectDataMigration004(Session())

        session.close()


    def down(self,migrate_engine):
        Base.metadata.drop_all(bind=migrate_engine)
