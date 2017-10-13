# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2017

@author: rtorres
'''


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()
