# -*- coding: utf-8 -*-
'''
Created on 12-10-2017

@author: worktrial
'''
import os

import MySQLdb


class DAO():
    host = None
    user = None
    password = None
    db_name = None
    port = None
    conection = None

    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.port = int(os.getenv('DB_PORT', '3306'))

    def create_connection(self):
        self.conection = MySQLdb.connect(self.host, self.user, self.password, self.db_name, self.port)

    def close_connection(self):
        if self.conection:
            self.conection.close()

    def commit(self):
        if self.conection:
            self.conection.commit()

    def roll_bakc(self):
        if self.conection:
            self.conection.rollback()
