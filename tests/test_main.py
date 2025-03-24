from slurm_comunicator.comunicator import SlurmComms
import subprocess

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
    assert len(time_statistics.keys()) == 9

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

def test_number_of_large_long_jobs():

    comms = SlurmComms()
    raw_data = subprocess.run(['squeue', '-p', 'large-long', '-t', 'R'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
    number_of_jobs = len(raw_data.split('\n')) - 1

    all_job_data = comms.get_all_data_of_all_jobs()
    number_of_cores_per_partition = {}

    for job in all_job_data:
        partition = job['partition']
        number_of_cores = job['number_of_cores']

        if partition not in number_of_cores_per_partition.keys():
            number_of_cores_per_partition[partition] = [number_of_cores]
        else:
            number_of_cores_per_partition[partition].append(number_of_cores)

    assert number_of_jobs == len([cores for cores in number_of_cores_per_partition['large-long'] if cores != 0])
