# -*- coding: utf-8 *-*
import sys
sys.path.append('..')

import logging

from pymongo_logging import MongoHandler

if __name__ == '__main__':

    log = logging.getLogger('SimpleExample')
    log.setLevel(logging.DEBUG)

    log.addHandler(MongoHandler.to(database='ALOG', collection='log'))

    log.debug("1 - debug message")
    log.info("2 - info message")
    log.warning("3 - warn message")
    log.error("4 - error message")
    log.critical("5 - critical message")
