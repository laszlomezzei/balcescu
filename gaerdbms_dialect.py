__author__ = 'laszlomezzei'
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb
from sqlalchemy.pool import NullPool
import re

"""Support for Google Cloud SQL on Google App Engine

Connecting
-----------

Connect string format::

    mysql+gaerdbms:///<dbname>?instance=<project:instance>


  # Example:
  create_engine('mysql+gaerdbms:///mydb?instance=myproject:instance1')
"""


class MySQLDialect_gaerdbms(MySQLDialect_mysqldb):

    @classmethod
    def dbapi(cls):
        from google.appengine.api import apiproxy_stub_map

        if apiproxy_stub_map.apiproxy.GetStub('rdbms'):
            from google.storage.speckle.python.api import rdbms_apiproxy
            return rdbms_apiproxy
        else:
            from google.storage.speckle.python.api import rdbms_googleapi
            return rdbms_googleapi

    @classmethod
    def get_pool_class(cls, url):
        # Cloud SQL connections die at any moment
        return NullPool

    def create_connect_args(self, url):
        opts = url.translate_connect_args()
        opts['dsn'] = ''  # unused but required to pass to rdbms.connect()
        opts['instance'] = url.query['instance']
        return [], opts

    def _extract_error_code(self, exception):
        match = re.compile(r"^(\d+):").match(str(exception))
        code = match.group(1)
        if code:
            return int(code)

dialect = MySQLDialect_gaerdbms
