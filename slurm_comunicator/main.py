
from slurm_comunicator.comunicator import SlurmComms  # Class names should be PascalCase
from slurm_comunicator.utils import *
import numpy as np
import shutil

def add(x,y):
    return x+y


if __name__ == '__main__':

    terminal_width = shutil.get_terminal_size().columns
    terminal_height = shutil.get_terminal_size().lines

    print('#'*(terminal_width//2))
    for i in range(terminal_height//4):
        if i == (terminal_height//4):
            print('#' + ' '*((terminal_width//5)-2) + 'Slurm Comunicator' + ' '*((terminal_width//5)-2) + '#')
        print('#' + ' '*((terminal_width//2)-2) + '#')
    print('#'*(terminal_width//2))
    print('\n')

    comms = SlurmComms()

    number_of_cores_check = True
    average_length_of_job_check = False
    check_partition_useage = True

    if number_of_cores_check == True:
        ## Get statistics on the number of cores being used ##
        total_cores_used = comms.get_total_number_of_cores_in_use()
        print(f'Total cores used: {total_cores_used}, {100*(total_cores_used/15102):.2f}% of the HPC is currently being used.')

    if average_length_of_job_check == True:
        ## Determine the average length of time of a job ##
        time_statistics = comms.get_elapsed_time_of_jobs_over_last_24_hours()
        run_time = time_statistics['run_times']
        requested_time = time_statistics['requested_time']
        save_array_as_excel(time_statistics, 'time_statistics')
        average_run_time = np.average(run_time)
        average_requested_time = np.average(requested_time)
        print(f'Average requested time over last 24 hours: {convert_minuets_in_to_time_string(average_requested_time)}')
        print(f'Average run time over last 24 hours: {convert_minuets_in_to_time_string(average_run_time)}')

    if check_partition_useage == True:
        ## Determine the amounts of jobs currently running in each parition ##
        print('\n')
        print('#'*(terminal_width//2))
        print('Partition Data')
        print('#'*(terminal_width//2))
        print('\n')
        all_job_data = comms.get_all_data_of_all_jobs()
        number_of_cores_per_partition = {}

        for job in all_job_data:
            partition = job['partition']
            number_of_cores = job['number_of_cores']

            if partition not in number_of_cores_per_partition.keys():
                number_of_cores_per_partition[partition] = [number_of_cores]
            else:
                number_of_cores_per_partition[partition].append(number_of_cores)
        
        for partition in number_of_cores_per_partition.keys():
            print(f'Partition: {partition}, {len(number_of_cores_per_partition[partition])} jobs currently running, {sum(number_of_cores_per_partition[partition])} cores in use.')



        