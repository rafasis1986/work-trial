# -*- coding: utf-8 -*-
'''
Created on 16-10-2017

@author: worktrial
'''

from facades import worktrialfacade as f
from snippets import queries as q


def test_get_tubes_id():
    q.init_worktrial_scripts()
    response = q.get_tube_ids()
    f.find_aborted_and_pending_ssr()
    assert len(response) == 10


def test_get_aborted_ssr_list():
    response = q.get_rows_table('aborted_ssr')
    assert len(response) == 8


def test_get_pending_ssr_list():
    response = q.get_rows_table('pending_ssr')
    assert len(response) == 4


def test_abortable_ssr_with_results():
    response = q.get_ssr_with_results()
    assert len(response) == 2


def test_prid_abortables_totals():
    prids = q.get_prid_abort_ssr_totals()
    for p in prids:
        if p['prid'] == '10-10-2016-90':
            assert p['abort_ssr'] == p['total_ssr']
        else:
            assert p['abort_ssr'] < p['total_ssr']
