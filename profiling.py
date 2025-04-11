
from slurm_comunicator.comunicator import SlurmComms  
from slurm_comunicator.utils import *
import numpy as np
import shutil
from datetime import date
import line_profiler


def print_results():

    terminal_width = shutil.get_terminal_size().columns
    terminal_height = shutil.get_terminal_size().lines

    comms = SlurmComms(prometheus_comparison=False)


    comms.get_partitions()
    global_quantities = {'date': date.today(), 
                            'total_number_of_cores' : comms.get_total_cores_in_use(),
                            'jobs_pending_in_the_queue' : comms.get_n_pending_jobs_in_queue(),
                            'jobs_running_in_the_queue' : comms.get_n_running_jobs_in_queue()}

    partition_dictionary_n_cores = comms.get_n_cores_partition_dictionary()
    partition_dictionary_n_jobs = comms.get_n_jobs_partition_dictionary()
    total_cores_in_use = comms.get_total_cores_in_use()
    total_cores_in_cluster = comms.total_cores_in_cluster

    print(partition_dictionary_n_cores)
    #print(partition_dictionary_n_jobs)

    print(f'Currently {total_cores_in_use} cores are in use out of {total_cores_in_cluster} cores in the cluster.')
    print(f'Currently {(total_cores_in_use/total_cores_in_cluster)*100:.2f}/% of the cluster is in use.')
    print(f'There are {global_quantities["jobs_pending_in_the_queue"]} jobs pending in the queue.')
    print(f'There are {global_quantities["jobs_running_in_the_queue"]} jobs running in the queue.')

def print_new_section(title: str, terminal_width) -> None:
    print('\n')
    print('#'*(terminal_width//2))
    print(title)
    print('#'*(terminal_width//2))
    print('\n')

if __name__ == '__main__':
    '''
        I should probably abstract some of this code into functions,
        it has ended up much longer than I had anticipated.
    '''
    print_results()
