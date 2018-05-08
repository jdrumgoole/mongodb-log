# -*- coding: utf-8 *-*
import logging
import unittest

from pymongo_logging import MongoHandler

import pymongo


class TestAuth(unittest.TestCase):

    def setUp(self):
        """ Create an empty database that could be used for logging """
        self._dbname = '_mongolog_auth'
        self._collection_name = 'log'
        self._username = 'MyUsername'
        self._password = 'MySeCrEtPaSsWoRd'

        self._conn = pymongo.MongoClient()
        self._db = self._conn[self._dbname]
        self._collection = self._db[self._collection_name]

        try:
            self._db.command( "dropUser", self._username)
        except pymongo.errors.OperationFailure:
            pass
        self._db.command("createUser", self._username, pwd=self._password, roles=["readWrite"])
        #self._db.add_user(self._username, self._password)

    def tearDown(self):
        """ Drop used database """
        self._conn.drop_database(self._dbname)
        self._db.command( "dropUser", self._username)

    def testAuthentication(self):
        """ Logging example with authentication """
        log = logging.getLogger('authentication')

        uri = "mongodb://" + self._username + ":" + self._password + "@localhost/" + self._dbname
        log.addHandler(MongoHandler(mongodb_uri=uri, database=self._db, collection=self._collection))

        log.error('test')

        message = self._collection.find_one({'levelname': 'ERROR',
                                              'msg': 'test'})

        #print("uri:{}".format(uri))
        # for i in self._collection.find() :
        #     print(i)

        self.assertEqual(message['msg'], 'test')

if __name__ == '__main__':
    unittest.main()