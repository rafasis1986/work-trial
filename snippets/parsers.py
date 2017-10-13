# -*- coding: utf-8 -*-
'''
Created on 12-10-2017

@author: worktrial
'''
from datetime import datetime


def get_days_elapsed(prid):
    d1 = datetime.strptime(prid[:10], '%m-%d-%Y').date()
    d2 = datetime.now().date()
    return abs((d2 - d1).days)
