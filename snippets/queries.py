# -*- coding: utf-8 -*-
'''
Created on 12-10-2017

@author: worktrial
'''
import sys

from MySQLdb import Error as DBError
from MySQLdb.cursors import DictCursor

from .dao import DAO as dao
from .logger import Logger as log
from .parsers import get_days_elapsed


def init_worktrial_scripts():
    try:
        for s in ['aborted', 'pending']:
            query_str = 'TRUNCATE {0}_ssr ;'.format(s)
            dao.create_connection()
            cur = dao.conection.cursor()
            cur.execute(query_str)
            dao.commit()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_tube_ids():
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        query_str = 'SELECT distinct(tubeid) FROM samples_view ORDER BY tubeid;'
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_ssr_list_from_tube_id(tube_id):
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        fields = 'lsl.tubeid as tubeid, lsl.id as ssr, lsl.prid, lpt.seqRunId'
        tables = 'Lab_Sample_Loading as lsl'
        conditions = 'lsl.tubeid="{0}"'.format(tube_id)
        criteria_order = 'lsl.id desc'
        join = 'Lab_Pipeline_Tracking as lpt ON lpt.PRID = lsl.PRID'
        query_str = 'SELECT {0} FROM {1} INNER JOIN {2} WHERE {3} ORDER BY {4};'.format(
            fields,
            tables,
            join,
            conditions,
            criteria_order,
        )
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_ssr_with_results():
    try:
        dao.create_connection()
        ssr_list = list()
        for q in ['clinical', 'results']:
            query_str = 'SELECT ssr FROM aborted_in_%s_view;' % q
            cur = dao.conection.cursor(DictCursor)
            cur.execute(query_str)
            aux_rows = cur.fetchall()
            ssr_list += [a['ssr'] for a in aux_rows]
        return ssr_list
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def get_prid_abort_ssr_totals():
    try:
        dao.create_connection()
        query_str = 'SELECT * FROM prid_abort_ssr_totals_view;'
        cur = dao.conection.cursor(DictCursor)
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def get_rows_table(table_name=''):
    try:
        dao.create_connection()
        query_str = 'SELECT * FROM {0};'.format(table_name)
        cur = dao.conection.cursor(DictCursor)
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def insert_filtered_ssr(status, ssr_list):
    if len(ssr_list) > 0:
        try:
            query_values = ''
            for row in ssr_list:
                days = get_days_elapsed(row['prid'])
                value = ('("{0}","{1}",{2},{3},{4}),'.format(
                    str(row['tubeid']),
                    row['prid'],
                    days,
                    row['ssr'],
                    row['prid'].split('-')[-1],
                ))
                query_values += value
            values_str = 'tubeid, prid, days_elapsed, ssr, prid_id'
            query_str = 'INSERT INTO {0}_ssr ({1}) VALUES {2};'.format(
                status,
                values_str,
                query_values[:-1],
            )
            dao.create_connection()
            cur = dao.conection.cursor(DictCursor)
            cur.execute(query_str)
            dao.commit()
        except DBError as e:
            log.warning('Error %d: %s' % (e.args[0], e.args[1]))
            dao.roll_bakc()
        except Exception as e:
            log.critical('Error %d: %s' % (e.args[0], e.args[1]))
            dao.close_connection()


def update_aborted_ssr_results(ssr_list=[]):
    try:
        dao.create_connection()
        fields = 'result = 0'
        ssr_str = '-1'
        if len(ssr_list) > 0:
            ssr_str = ','.join([str(item) for item in ssr_list])
        condition = 'ssr not in ({0})'.format(ssr_str)
        query_str = 'UPDATE aborted_ssr SET {0}  WHERE {1};'.format(
            fields,
            condition)
        cur = dao.conection.cursor()
        cur.execute(query_str)
        dao.commit()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()
