
from slurm_comunicator.comunicator import SlurmComms  
from slurm_comunicator.utils import *
import numpy as np
import shutil
from datetime import date

def add(x,y):
    return x+y


def print_new_section(title: str, terminal_width) -> None:
    print('\n')
    print('#'*(terminal_width//2))
    print(title)
    print('#'*(terminal_width//2))
    print('\n')


if __name__ == '__main__':

    terminal_width = shutil.get_terminal_size().columns
    terminal_height = shutil.get_terminal_size().lines
    quantities_of_interest = {'date': date.today(), 'number_of_cores' : 0, 'average_length_of_job' : 0, 'jobs_in_the_queue' : 0,
                              '' : 0, 'large-long' : 0, 'large-sho+' : 0, 'small-long' : 0, 'interacti+' : 0}

    print_new_section('Slurm Comunicator', terminal_width)

    comms = SlurmComms()

    number_of_cores_check = False
    average_length_of_job_check = False
    check_partition_useage = False
    print_csv_file_check = True
    append_to_csv_check = True

    if number_of_cores_check == True:
        ## Get statistics on the number of cores being used ##
        total_cores_used = comms.get_total_number_of_cores_in_use()
        print(f'Total cores used: {total_cores_used}, {100*(total_cores_used/15102):.2f}% of the HPC is currently being used.')
        quantities_of_interest['number_of_cores'] = total_cores_used

    if average_length_of_job_check == True:
        ## Determine the average length of time of a job ##
        print_new_section('Average Job Length - last 24 hours', terminal_width)
        time_statistics = comms.get_elapsed_time_of_jobs_over_last_24_hours()
        run_time = time_statistics['run_times']
        requested_time = time_statistics['requested_time']
        save_array_as_excel(time_statistics, 'time_statistics')
        average_run_time = np.average(run_time)
        average_requested_time = np.average(requested_time)
        print(f'Average requested time over last 24 hours: {convert_minuets_in_to_time_string(average_requested_time)}')
        print(f'Average run time over last 24 hours: {convert_minuets_in_to_time_string(average_run_time)}')
        quantities_of_interest['average_length_of_job'] = average_run_time

    if check_partition_useage == True:
        ## Determine the amounts of jobs currently running in each parition ##
        print_new_section('Partition Useage', terminal_width)
        all_job_data = comms.get_all_data_of_all_jobs()
        number_of_cores_per_partition = {}

        for job in all_job_data:
            partition = job['partition']
            number_of_cores = job['number_of_cores']

            if partition not in number_of_cores_per_partition.keys():
                number_of_cores_per_partition[partition] = [number_of_cores]
            else:
                number_of_cores_per_partition[partition].append(number_of_cores)
        
        print(number_of_cores_per_partition)
        print('\n')
        for partition in number_of_cores_per_partition.keys():

            number_of_running_jobs = 0
            total_cores_used = 0
            for cores in number_of_cores_per_partition[partition]:
                if cores > 0:
                    number_of_running_jobs += 1
                    total_cores_used += cores
            quantities_of_interest[partition] = number_of_running_jobs
            print(f'''Partition: {partition if partition != '' else 'Queue'}, {number_of_running_jobs}
                   jobs currently running, {sum(number_of_cores_per_partition[partition])} cores in use.
                   Average number of cores per job: {total_cores_used / number_of_running_jobs if number_of_running_jobs != 0 else 0:.0f}.''')
        print('\n')

    if append_to_csv_check == True:
        append_to_csv(quantities_of_interest)

    if print_csv_file_check == True:
        print_csv_file()