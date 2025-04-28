from slurm_comunicator.comunicator import SlurmComms  
from slurm_comunicator.utils import *
import numpy as np
import shutil
from datetime import date
import pyfiglet


def print_new_section(title: str, terminal_width) -> None:
    print('\n')
    print('#'*(terminal_width//2))
    print(title)
    print('#'*(terminal_width//2))
    print('\n')


if __name__ == '__main__':
    
    terminal_width = shutil.get_terminal_size().columns
    terminal_height = shutil.get_terminal_size().lines

    print('-'*int(0.7*terminal_width))
    print(pyfiglet.figlet_format("SlurmExporter", font="slant"))
    comms = SlurmComms(prometheus_comparison=False)
    comms.get_partitions()

    global_quantities = {'date': date.today(), 
                            'total_number_of_cores' : comms.get_total_cores_in_use(),
                            'jobs_pending_in_the_queue' : comms.get_n_pending_jobs_in_queue(),
                            'jobs_running_in_the_queue' : comms.get_n_running_jobs_in_queue()}

    partition_dictionary_n_cores = comms.get_n_cores_partition_dictionary()
    partition_dictionary_n_jobs = comms.get_n_jobs_partition_dictionary()
    partition_dictionary_wait_times = comms.get_average_wait_time_partition_dictionary()
    queue_length_dictionary = comms.get_queue_length_partition_dictionary()

    total_cores_in_use = comms.total_cores_in_use
    total_cores_in_cluster = comms.total_cores_in_cluster

    manage_csv_file([partition_dictionary_n_cores], f'number_of_cores-{date.today()}.csv')
    manage_csv_file([partition_dictionary_n_jobs], f'number_of_jobs-{date.today()}.csv')
    manage_csv_file([partition_dictionary_wait_times], f'wait_times-{date.today()}.csv')
    manage_csv_file([queue_length_dictionary], f'jobs_pending-{date.today()}.csv')

    print('-'*int(0.7*terminal_width))
    print(f'Cores dictionary: {partition_dictionary_n_cores}')
    print(f'Jobs dictionary: {partition_dictionary_n_jobs}')
    print(f'Wait times dictionary: {partition_dictionary_wait_times}')
    print(f'Jobs pending dictionary: {queue_length_dictionary}')
    print('-'*int(0.7*terminal_width))
    print(f'Currently {total_cores_in_use} cores are in use out of {total_cores_in_cluster} cores in the cluster.')
    print(f'Currently {(total_cores_in_use/total_cores_in_cluster)*100:.2f}/% of the cluster is in use.')
    print('-'*int(0.7*terminal_width))
    print(f'There are {global_quantities["jobs_pending_in_the_queue"]} jobs pending in the queue.')
    print(f'There are {global_quantities["jobs_running_in_the_queue"]} jobs running in the queue.')
