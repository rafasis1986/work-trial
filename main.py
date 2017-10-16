# -*- coding: utf-8 -*-
# !/usr/bin/env python
'''
Created on Oct 15, 2017

@author: rtorres
'''
from cement.core.foundation import CementApp

from controllers.basecontroller import BaseController
from utils import constants as c


class WorkTrialApp(CementApp):

    class Meta:
        label = c.APP_NAME
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [BaseController]


def main():
    with WorkTrialApp() as app:
        app.run()


if __name__ == '__main__':
    main()
