from slurm_comunicator.comunicator import SlurmComms

def test_elapsed_time_of_jobs_over_last_24_hours_per_partition():
    comms = SlurmComms()
    time_statistics = comms.elapsed_time_of_jobs_over_last_24_hours_per_partition()
    assert isinstance(time_statistics, dict)
    assert 'large-long' in time_statistics.keys()
    assert 'large-sho+' in time_statistics.keys()
    assert 'small-long' in time_statistics.keys()
    assert 'interacti+' in time_statistics.keys()
    assert 'debug' in time_statistics.keys()
    assert 'small-sho+' in time_statistics.keys()
    assert len(time_statistics.keys()) == 7

def test_get_all_data_of_all_jobs():
    comms = SlurmComms()
    all_job_data = comms.get_all_data_of_all_jobs()
    assert isinstance(all_job_data, list)
    assert isinstance(all_job_data[0], dict)
    assert 'partition' in all_job_data[0].keys()
    assert 'number_of_cores' in all_job_data[0].keys()
    assert 'job_id' in all_job_data[0].keys()
    assert 'account' in all_job_data[0].keys()
    assert 'account_name' in all_job_data[0].keys()