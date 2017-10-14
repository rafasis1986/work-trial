# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2017

@author: rtorres
'''
import logging
from snippets.singleton import singleton


@singleton
class Logger():

    def __init__(self):
        logging.basicConfig(
            level=10,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            filename='trial.log')
        self.logr = logging.getLogger('root')

    def error(self, msg):
        self.logr.error(msg)

    def info(self, msg):
        self.logr.info(msg)

    def debug(self, msg):
        self.logr.debug(msg)

    def warning(self, msg):
        self.logr.warning(msg)

    def critical(self, msg):
        self.logr.critical(msg)
