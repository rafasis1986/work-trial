# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: rtorres
'''
import time

from snippets import queries as q
from snippets.logger import Logger as log
from snippets.parsers import get_days_elapsed


def find_aborted_and_pending_ssr():
    try:
        log.debug('start get_aborted_and_pending_ssr')
        start_time = time.time()
        q.init_worktrial_scripts()
        samples = q.get_sample_ids()
        counter = 1
        print 'I found {0} samples to analyze'.format(len(samples))
        for s in samples:
            print 'I am analizing the sample {0} from  {1}, current id {2}'.format(
                counter,
                len(samples),
                s['sample'])
            counter += 1
            first_processed = False
            pending_candidates = list()
            aborted_candidates = list()
            response = q.get_ssr_list_from_sample_id(s['sample'])
            for row in response:
                if row['seqRunId'] != 0:
                    if not first_processed:
                        first_processed = True
                else:
                    if first_processed:
                        aborted_candidates.append(row)
                    else:
                        pending_candidates.append(row)
            if not first_processed:
                q.insert_exclude_sample(s)
            else:
                q.insert_filtered_ssr('aborted', aborted_candidates)
                q.insert_filtered_ssr('pending', pending_candidates)
    except Exception as e:
        log.critical('Error {0}: {1}'.format(type(e), e.message))
    finally:
        t_str = 'time elapsed {0} second !'.format(time.time() - start_time)
        log.debug(t_str)
        log.debug('end get_aborted_and_pending_ssr')


def check_aborted_ssr():
    try:
        log.debug('start check_aborted_ssr')
        ssr_list = q.get_ssr_with_results()
        q.update_aborted_ssr_results(ssr_list)
        print 'Checked {0} SSR records'.format(len(ssr_list))
    except Exception as e:
        log.critical('Error {0}: {1}'.format(type(e), e.message))
    finally:
        log.debug('end check_aborted_ssr')


def filter_prid_abortables(only_erasables=False, days_filter=False, limit=180):
    try:
        log.debug('start filter_prid_abortables')
        prid_totals = q.get_prid_abort_ssr_totals()
        prids = list()
        for p in prid_totals:
            aborted = float(p['abort_ssr'])
            total = float(p['total_ssr'])
            per_abort = (aborted / total) * 100
            days_elapsed = get_days_elapsed(p['prid'])
            erasable = False
            if per_abort == 100:
                erasable = True
            elif days_filter and days_elapsed > limit:
                erasable = True
            p.update({'percentage': per_abort})
            p.update({'days_elapsed': days_elapsed})
            if only_erasables and not erasable:
                pass
            else:
                aux = [
                    p['prid'],
                    p['abort_ssr'],
                    p['total_ssr'],
                    '{:3.2f}'.format(per_abort),
                    days_elapsed,
                    erasable]
                prids.append(aux)
        return prids
    except Exception as e:
        log.critical('Error {0}: {1}'.format(type(e), e.message))
    finally:
        log.debug('end filter_prid_abortables')


def make_report_output(file_name, absolutes_prids=[], partials_prids=[]):
    try:
        log.debug('start make_report_output')
        report = open(file_name, 'w')
        report.write('PRIDs to remove absolutely: {0} \n'.format(','.join(absolutes_prids)))
        if len(absolutes_prids) > 0:
            ssr_ids = q.get_ssr_abort_list_from_prids(absolutes_prids)
            if ssr_ids:
                ssr_ids = ['%s' % str(ssr['id']) for ssr in ssr_ids]
                report.write('SSR: {0} \n'.format(','.join(ssr_ids)))
        if len(partials_prids) > 0:
            report.write('\n')
            report.write('SSR list from partial PRIDs to remove \n')
            ssr_ids = q.get_ssr_abort_list_from_prids(partials_prids)
            if ssr_ids:
                ssr_ids = ['%s' % str(ssr['id']) for ssr in ssr_ids]
                report.write('SSR: {0} \n'.format(','.join(ssr_ids)))
        report.close()
        print 'Generated report in {0}'.format(file_name)
    except Exception as e:
        log.critical('Error {0}: {1}'.format(type(e), e.message))
    finally:
        log.debug('end make_report_output')
