# -*- coding: utf-8 -*-
# !/usr/bin/env python
'''
Created on 12-10-2017

@author: worktrial
'''
import time

from snippets import queries as q
from snippets.logger import Logger as log


if __name__ == '__main__':
    start_time = time.time()
    try:
        samples = q.get_sample_ids()
        exclude_samples = list()
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
        print 'The script took {0} second !'.format(time.time() - start_time)
