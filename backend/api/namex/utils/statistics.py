def get_waiting_time(examination_time_secs, queue_requests):
    waiting_time = (
        0.0
        if (examination_time_secs is None or queue_requests is None)
        else round(examination_time_secs * queue_requests / 86400)
    )

    return waiting_time
