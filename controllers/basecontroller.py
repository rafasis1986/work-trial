# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: rtorres
'''
import os

from cement.core.controller import CementBaseController
from cement.core.controller import expose
from cement.utils import shell
from facades import worktrialfacade as f
from snippets.decisionprompt import DecisionPrompt
from utils import constants as c


class BaseController(CementBaseController):
    absolute_prids = []
    partial_prids = []

    class Meta:
        label = 'base'
        description = 'this is the menu with all options'

    @expose(hide=True)
    def default(self):
        try:
            while True:
                option = shell.Prompt(
                    "What do you want to do?",
                    options=[
                        c.MENU_FILTER_SSR,
                        c.MENU_FILTER_PRID,
                        c.MENU_GET_REPORT_PRID,
                        c.MENU_GET_ROWS_ID_TO_DELETE,
                        c.MENU_CLOSE],
                    numbered=True,)
                if option.input == c.MENU_CLOSE:
                    print 'good bye'
                    break
                elif option.input == c.MENU_FILTER_SSR:
                    f.find_aborted_and_pending_ssr()
                elif option.input == c.MENU_FILTER_PRID:
                    f.check_aborted_ssr()
                elif option.input == c.MENU_GET_ROWS_ID_TO_DELETE:
                    print 'Please insert the filename to get all id rows selected.'
                    file_name = ''
                    while len(file_name) == 0:
                        file_name = raw_input('file name: ')
                    f.make_report_output(file_name, self.absolute_prids, self.partial_prids)
                elif option.input == c.MENU_GET_REPORT_PRID:
                    self.absolute_prids = []
                    self.partial_prids = []
                    decision = DecisionPrompt('Do you want get only erasable prids?')
                    erasable = False
                    if decision.input.lower() == 'yes':
                        erasable = True
                    limit_days = int(os.getenv('DAYS_EXPIRES', 180))
                    question = 'do you want delete the prids with more than {0} days elapsed?'.format(limit_days)
                    decision = DecisionPrompt(question)
                    days_filter = False
                    if decision.input.lower() == 'yes':
                        days_filter = True
                    prids = f.filter_prid_abortables(
                        only_erasables=erasable,
                        days_filter=days_filter,
                        limit=limit_days)
                    headers = [
                        'PRID', 'Aborted SSR', 'Total SSR', 'Percentage', 'Days Elapsed', 'Erasable']
                    self.app.render(prids, headers=headers)
                    for p in prids:
                        if p[-1]:
                            self.absolute_prids.append(p[0])
                        else:
                            self.partial_prids.append(p[0])
                print('')
        except Exception as e:
            print type(e), e
