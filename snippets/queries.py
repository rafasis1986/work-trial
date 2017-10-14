# -*- coding: utf-8 -*-
'''
Created on 12-10-2017

@author: worktrial
'''
import sys

from MySQLdb.cursors import DictCursor
from MySQLdb import Error as DBError

from .dao import DAO
from .parsers import get_days_elapsed
from .logger import Logger as log


def get_sample_ids():
    dao = DAO()
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        query_str = 'SELECT distinct(sample) FROM test.samples_view ORDER BY sample;'
        cur.execute(query_str)
        return cur.fetchall()
    except DBError as e:
        log.critical('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        dao.close_connection()


def get_ssr_list_from_sample_id(sample_id):
    dao = DAO()
    try:
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        fields = 's.id as sample, lsl.tubeid as tubeid, lsl.id as ssr, lsl.prid, lpt.seqRunId'
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


def insert_filtered_ssr(status, ssr_list):
    if len(ssr_list) > 0:
        dao = DAO()
        try:
            query_values = ''
            for row in ssr_list:
                days = get_days_elapsed(row['prid'])
                value = ('({0},"{1}","{2}",{3},{4}),'.format(
                    row['sample'],
                    str(row['tubeid']),
                    row['prid'],
                    days,
                    row['ssr'],
                ))
                query_values += value
            values_str = 'sample, tubeid, prid, days_elapsed, ssr'
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


def insert_exclude_sample(sample):
    dao = DAO()
    try:
        values_str = 'id'
        query_str = 'INSERT INTO exclude_samples ({0}) VALUES ({1});'.format(
            values_str,
            sample['sample'],
        )
        dao.create_connection()
        cur = dao.conection.cursor(DictCursor)
        cur.execute(query_str)
        dao.commit()
    except DBError as e:
        log.warning('Error %d: %s' % (e.args[0], e.args[1]))
        dao.roll_bakc()
    finally:
        dao.close_connection()
