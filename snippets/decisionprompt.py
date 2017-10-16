# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: rtorres
'''
from cement.utils.shell import Prompt


class DecisionPrompt(Prompt):

    class Meta:
        text = "Do you agree?"
        options = ['Yes', 'no']
        options_separator = '|'
        default = 'no'
        clear = True
        max_attempts = 10
