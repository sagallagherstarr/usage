#
# from contextlib import contextmanager

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin db.__init__")

import constants

from peewee import SqliteDatabase

allModels = set()
log.debug("allModels is %s", allModels)

class DatabaseConnection:
    def __init__(self, sqliteFileName, testing=False):
        self.fileName = sqliteFileName
        self.testing = testing
        
        self.peeweeDbConnection = None
    
    def prepareConnection(self):
        self.peeweeDbConnection = SqliteDatabase(constants.dbFileName, pragmas={
            'journal_mode': 'wal',
            'cache_size': 10000,  # 10000 pages, or ~40MB
            'foreign_keys': 1,  # Enforce foreign-key constraints
        })
        
    def openConnection(self):
        self.peeweeDbConnection.connect(reuse_if_open=True)
    
    def closeConnection(self):
        self.peeweeDbConnection.close()
    
    def contextManager(self):
        return self.peeweeDbConnection.connection_context()

    def createTables(self, drop_first=False):
        """Because we delay creating the database until
           after modules are imported, we have to bind
           Model classes to the database at this point.
           Fortunately, we're already set up to do that
           """
        self.peeweeDbConnection.bind(allModels)
        
        with self.peeweeDbConnection.connection_context():
            if drop_first:
                self.peeweeDbConnection.drop_tables(allModels, safe=True)
                
            self.peeweeDbConnection.create_tables(allModels)

def registerModel(klass):
    log.debug("registerModel: klass is %s", klass)
    allModels.add(klass)
    
    return klass


