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
        query_str = 'TRUNCATE aborted_ssr ;'
        dao.create_connection()
        cur = dao.conection.cursor()
        cur.execute(query_str)
        dao.commit()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_sample_ids():
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        query_str = 'SELECT distinct(sample) FROM samples_view ORDER BY sample;'
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_ssr_list_from_sample_id(sample_id):
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        fields = 's.id as sample, lsl.tubeid as tubeid, lsl.id as ssr, lsl.prid, lpt.seqRunId, lpt.id as prid_id'
        tables = 'samples as s'
        conditions = 's.id={0}'.format(sample_id)
        criteria_order = 'lsl.id desc'
        first_join = 'Lab_Sample_Loading as lsl ON lsl.tubeId = s.vial_barcode'
        second_join = 'Lab_Pipeline_Tracking as lpt ON lpt.PRID = lsl.PRID'
        query_str = 'SELECT {0} FROM {1} INNER JOIN {2} INNER JOIN {3} WHERE {4} ORDER BY {5};'.format(
            fields,
            tables,
            first_join,
            second_join,
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


def get_rows_by_table_name(table_name, condition=None):
    try:
        dao.create_connection()
        if condition:
            query_str = 'SELECT * FROM {0} WHERE {1};'.format(
                table_name,
                condition)
        else:
            query_str = 'SELECT * FROM {0};'.format(table_name)
        cur = dao.conection.cursor(DictCursor)
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def get_ssr_abort_list_from_prids(prids):
    try:
        dao.create_connection()
        condition = ''
        for p in prids:
            condition += '"{0}",'.format(p)
        if len(condition) > 0:
            condition = condition[:-1]
        query_str = 'SELECT id FROM Lab_Sample_Loading WHERE prid in ({0}) order by id;'.format(condition)
        cur = dao.conection.cursor(DictCursor)
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def insert_filtered_ssr(pending, ssr_list):
    if len(ssr_list) > 0:
        try:
            query_values = ''
            for row in ssr_list:
                days = get_days_elapsed(row['prid'])
                value = ('({0},"{1}","{2}",{3},{4}, {5}, {6}),'.format(
                    row['sample'],
                    str(row['tubeid']),
                    row['prid'],
                    days,
                    row['ssr'],
                    row['prid_id'],
                    pending,
                ))
                query_values += value
            values_str = 'sample, tubeid, prid, days_elapsed, ssr, prid_id, pending'
            query_str = 'INSERT INTO aborted_ssr ({0}) VALUES {1};'.format(
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


def insert_exclude_sample(sample):
    try:
        values_str = 'id'
        query_str = 'INSERT INTO exclude_samples ({0}) VALUES ({1});'.format(
            values_str,
            sample['sample'],
        )
        dao.create_connection()
        cur = dao.conection.cursor()
        cur.execute(query_str)
        dao.commit()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()


def update_aborted_ssr_results(ssr_list=[]):
    try:
        dao.create_connection()
        fields = 'result = 0'
        ssr_str = '-1'
        if len(ssr_list) > 0:
            ssr_str = ','.join([str(item) for item in ssr_list])
        condition = 'ssr not in ({0})'.format(ssr_str)
        query_str = 'UPDATE aborted_ssr SET {0}  WHERE pending = 0 AND {1};'.format(
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
