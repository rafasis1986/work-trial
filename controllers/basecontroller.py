# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: rtorres
'''
from utils import constants as c
from cement.core.controller import CementBaseController
from cement.core.controller import expose
from cement.utils import shell
from facades import worktrialfacade as f
from snippets.decisionprompt import DecisionPrompt
import os


class BaseController(CementBaseController):

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
                        c.MENU_CLOSE],
                    numbered=True,)
                if option.input == c.MENU_CLOSE:
                    print 'good bye'
                    break
                elif option.input == c.MENU_FILTER_SSR:
                    f.find_aborted_and_pending_ssr()
                elif option.input == c.MENU_FILTER_PRID:
                    f.check_aborted_ssr()
                elif option.input == c.MENU_GET_REPORT_PRID:
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
                        'PRID', 'Total SSR', 'Aborted SSR', 'Percentage', 'Days Elapsed', 'Erasable']
                    self.app.render(prids, headers=headers)
                print('')
        except Exception as e:
            print type(e), e
