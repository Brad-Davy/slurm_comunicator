from slurm_comunicator import slurm_comms 
from utils import *
import numpy as np 

if __name__ == '__main__':

    
    comms = slurm_comms()

    ## Get statistics on the number of cores being used
    #total_cores_used = comms.get_total_number_of_cores_in_use()
    #print(f'Total cores used: {total_cores_used}, {100*(total_cores_used/15102):.2f}% of the HPC is currently being used.')
    #save_array_as_excel(comms.get_all_data_of_all_jobs(), 'output')

    ## Determine the average length of time of a job
    time_statistics = comms.get_elapsed_time_of_jobs_over_last_24_hours()
    run_time = time_statistics['run_times']
    requested_time = time_statistics['requested_time']
    save_array_as_excel(time_statistics, 'time_statistics')
    average_run_time = np.average(run_time)
    average_requested_time = np.average(requested_time)
    print(f'Average requested time over last 24 hours: {convert_minuets_in_to_time_string(average_requested_time)}')
    print(f'Average run time over last 24 hours: {convert_minuets_in_to_time_string(average_run_time)}')

