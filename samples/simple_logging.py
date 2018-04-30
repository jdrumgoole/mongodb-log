# -*- coding: utf-8 *-*
import sys
sys.path.append('..')

import logging

from pymongo_log import MongoHandler

if __name__ == '__main__':

    log = logging.getLogger('example')
    log.setLevel(logging.DEBUG)

    log.addHandler(MongoHandler.to('pymongo_log', 'log'))

    log.debug("1 - debug message")
    log.info("2 - info message")
    log.warn("3 - warn message")
    log.error("4 - error message")
    log.critical("5 - critical message")
