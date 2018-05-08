# -*- coding: utf-8 *-*
import logging
import unittest
import random
import string

from pymongo_logging import MongoHandler

import pymongo

class TestRootLoggerHandler(unittest.TestCase):
    """
    Test Handler attached to RootLogger
    """
    def setUp(self):
        """ Create an empty database that could be used for logging """
        self.db_name = '_mongolog_test'
        self.collection_name = 'log'

        self.conn = pymongo.MongoClient()
        self.db = self.conn[self.db_name]
        self.collection = self.db[self.collection_name]

        #self.conn.drop_database(self.db_name)

    def tearDown(self):
        """ Drop used database """
        #self.conn.drop_database(self.db_name)

    def testLogging(self):
        """ Simple logging example """
        log = logging.getLogger('log')
        log.setLevel(logging.DEBUG)
        handler = MongoHandler(mongodb_uri="mongodb://localhost:27017",
                               database=self.db_name,
                               collection=self.collection_name)

        self.assertEqual( handler.get_database().name, self.db_name)
        self.assertEqual( handler.get_collection().name, self.collection_name)
        log.addHandler(handler)

        log.debug('test')

        r = self.collection.find_one({'levelname': 'DEBUG', 'msg': 'test'})
        self.assertEqual(r['msg'], 'test')

    def testLoggingException(self):
        """ Logging example with exception """
        log = logging.getLogger('exception')
        log.setLevel(logging.DEBUG)
        log.addHandler(MongoHandler(mongodb_uri="mongodb://localhost:27017",
                                    database=self.db_name,
                                    collection=self.collection_name))

        try:
            1 / 0
        except ZeroDivisionError:
            log.error('test zero division', exc_info=True)

        r = self.collection.find_one({'levelname': 'ERROR',
            'msg': 'test zero division'})
        self.assertTrue(r['exc_info'].startswith('Traceback'))

    def testQueryableMessages(self):
        """ Logging example with dictionary """
        log = logging.getLogger('query')
        log.setLevel(logging.DEBUG)
        log.addHandler(MongoHandler(mongodb_uri="mongodb://localhost:27017",
                                    database=self.db,
                                    collection=self.collection))

        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        log.info({'address': '340 N 12th St', 'state': 'PA', 'country': 'US', "rand" : random_str })
        log.info({'address': '340 S 12th St', 'state': 'PA', 'country': 'US', "rand" : random_str })
        log.info({'address': '1234 Market St', 'state': 'PA', 'country': 'US', "rand" : random_str })

        # for i in self.collection.find():
        #     print(i)
            
        cursor = self.collection.find({'levelname'    : 'INFO',
                                       'msg.rand'     : random_str,
                                       'msg.address'  : '340 N 12th St'})

        self.assertEqual(cursor.count(), 1, "Expected query to return 1 "
            "message; it returned %d" % cursor.count())
        self.assertEqual(cursor[0]['msg']['address'], '340 N 12th St')

        cursor = self.collection.find({'levelname': 'INFO',
                                       'msg.state': 'PA',
                                        "msg.rand" : random_str })

        doc_count = cursor.count()
        self.assertEqual( doc_count, 3, "Didn't find all three documents:{}".format(doc_count))

if __name__ == '__main__':
    unittest.main()