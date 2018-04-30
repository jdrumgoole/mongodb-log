# -*- coding: utf-8 *-*
import logging
import unittest

from pymongo_log import MongoHandler
from os.path import dirname, join


from logging.config import fileConfig, dictConfig
import pymongo


class TestConfig(unittest.TestCase):

    def setUp(self):
        """ Create an empty database that could be used for logging """
        filename = join(dirname(__file__), 'logging-test.config')
        fileConfig(filename)

        self._dbname = '_mongolog_test'
        self._collection_name = 'log_test'

        self._conn = pymongo.MongoClient()
        self._db = self._conn[self._dbname]
        self._collection = self._db[self._collection_name]

        self._db.command("dropUser", "admin")
        self._db.command("createUser", "admin", pwd="password", roles=["readWrite"])

    def tearDown(self):
        """ Drop used database """
        self._conn.drop_database(self._dbname)

    def testLoggingFileConfiguration(self):
        log = logging.getLogger('example')
        log.addHandler(MongoHandler(mongodb_uri="mongodb://localhost:27017", database=self._dbname, collection=self._collection_name ))

        log.debug('test')

        message = self._collection.find_one({'levelname': 'DEBUG',
                                            'msg': 'test'})
        self.assertEqual(message['msg'], 'test')


class TestDictConfig(unittest.TestCase):

    def setUp(self):
        """ Create an empty database that could be used for logging """
        self._dbname = '_mongolog_test_dict'
        self._collection_name = 'log_test'

        self.configDict = {
            'version': 1,
            'handlers': {
                'mongo': {
                    'class': 'pymongo_log.handlers.MongoHandler',
                    "mongodb_uri" : 'mongodb://localhost:27017',
                    'database': self._dbname,
                    'collection': self._collection_name,
                    'level': 'INFO'
                }
            },
            'root': {
                'handlers': ['mongo'],
                'level': 'INFO'
            }
        }

        self._conn = pymongo.MongoClient()
        self._db = self._conn[self._dbname]
        self._collection = self._db[self._collection_name]

        self._conn.drop_database(self._dbname)

    def testLoggingDictConfiguration(self):

        dictConfig(self.configDict)

        log = logging.getLogger('dict_example')
        log.addHandler(MongoHandler( database=self._dbname, collection=self._collection_name))

        log.debug('testing dictionary config')

        message = self._collection.find_one({'levelname': 'DEBUG',
                                             'msg': 'dict_example'})
        self.assertEqual(message, None,
            "Logger put debug message in when info level handler requested")

        log.info('dict_example')
        message = self._collection.find_one({'levelname': 'INFO',
                                            'msg': 'dict_example'})
        self.assertNotEqual(message, None,
            "Logger didn't insert message into database")
        self.assertEqual(message['msg'], 'dict_example',
            "Logger didn't insert correct message into database")

    def tearDown(self):
        """ Drop used database """
        self._conn.drop_database(self._dbname)
