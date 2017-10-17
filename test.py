from snippets import queries as q
from facades.worktrialfacade import find_aborted_ssr, filter_prid_abortables


def test_get_samples_id():
    q.init_worktrial_scripts()
    response = q.get_sample_ids()
    find_aborted_ssr()
    assert len(response) == 9


def test_get_aborted_ssr_list():
    response = q.get_rows_by_table_name('aborted_ssr', 'pending=0')
    assert len(response) == 8


def test_get_pending_ssr_list():
    response = q.get_rows_by_table_name('aborted_ssr', 'pending=1')
    assert len(response) == 4


def test_abortable_ssr_with_results():
    response = q.get_ssr_with_results()
    assert len(response) == 2


def test_get_exclude_samples():
    response = q.get_rows_by_table_name('exclude_samples')
    assert len(response) == 1


def test_prid_abortables_without_legacy():
    ssr_list = q.get_ssr_with_results()
    q.update_aborted_ssr_results(ssr_list)
    prids = filter_prid_abortables(days_filter=False)
    count = 0
    for p in prids:
        if p[-1]:
            count += 1
    assert count == 1


def test_prid_abortables_with_legacy():
    prids = filter_prid_abortables(days_filter=True)
    assert len(prids) == 3
