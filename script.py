# -*- coding: utf-8 -*-
'''
Created on 12-10-2017

@author: worktrial
'''
from snippets import queries as q


if __name__ == "__main__":
    samples = q.get_sample_ids()
    exclude_samples = list()
    for s in samples:
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
