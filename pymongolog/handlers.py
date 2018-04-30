# -*- coding: utf-8 *-*
import sys
import getpass
import logging

from bson import InvalidDocument
from datetime import datetime
import pymongo
from socket import gethostname

if sys.version_info[0] >= 3:
    unicode = str

class MongoFormatter(logging.Formatter):
    def format(self, record):
        """Format exception object as a string"""
        data = record.__dict__.copy()

        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg

        data.update(
            username=getpass.getuser(),
            time=datetime.now(),
            host=gethostname(),
            message=msg,
            args=tuple(unicode(arg) for arg in record.args)
        )
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
        return data


class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo collection. This  handler is
    designed to be used with the standard python logging mechanism.
    """

    @classmethod
    def to(cls, mongodb_uri="mngodb://localhost:27017", database="AUDIT", collection="log",  level=logging.NOTSET):
        """ Create a handler for a given  """
        return cls(mongodb_uri, database, collection, level)

    def __init__(self, mongodb_uri="mongodb://localhost:27017", database="AUDIT", collection="log", level=logging.NOTSET):

        #print( " {} {} {} {}".format( mongodb_uri, database, collection, level))
        """ Init log handler and store the collection handle """
        logging.Handler.__init__(self, level)

        client = pymongo.MongoClient( host=mongodb_uri)

        if isinstance( database, str):
            self._database = client[database]
        elif isinstance( database, pymongo.database.Database):
            self._database = database
        else:
            raise TypeError( "'database' must be an instance of str or pymongo.database.Database")

        if isinstance(collection, str):
            self.collection = self._database[collection]
        elif isinstance(collection, pymongo.collection.Collection):
            self.collection = collection
        else:
            raise TypeError("'collection' must be an instance of str or pymongo.collection.Collection")

        self.formatter = MongoFormatter()

    def emit(self, record):
        """ Store the record to the collection. Async insert """
        try:
            self.collection.insert_one(self.format(record))
        except InvalidDocument as e:
            logging.error("Unable to save log record: %s", e.message,
                exc_info=True)
