from slurm_comunicator.main import add
from slurm_comunicator.comunicator import SlurmComms


def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

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
    