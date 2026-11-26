import operator

import django_rq


def test_default_queue_runs_job():
    queue = django_rq.get_queue("default", is_async=False)

    job = queue.enqueue(operator.add, 2, 3)

    assert job.is_finished
    assert job.return_value() == 5
