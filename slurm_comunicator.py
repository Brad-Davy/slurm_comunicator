import os
import subprocess
from datetime import datetime, timedelta

class slurm_comms:

    def __init__(self):
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        self.job_ids = []
        self.job_data = []
        self.fill_job_ids_array()


    def _get_current_job_information(self):
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def _get_number_of_cores(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> int:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()
	
        if len(split_job_information) == 4:
            return int(split_job_information[2])
        else:
            return 0 # quick fix for now, should add a bool arg which returns false if respone isnt valid (i.e. len() != 4).

    def _get_partition(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 4:
            return str(split_job_information[3])
        else:
            return ''


    def _get_account(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 4:
            return str(split_job_information[2])
        else:
            return ''

    def _get_account_name(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 4:
            return str(split_job_information[0])
        else:
            return ''

    def _get_individual_job_information(self, job_id: str) -> str:
        return subprocess.run(['sacct', '-j', job_id, '--format=User,Account,AllocCPUS,Partition'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def fill_job_ids_array(self):

        for lines in self.all_jobs_information.split('\n'):
            split_data = lines.split()
            if len(split_data) == 8:
                try:
                    self.job_ids.append(str(int(split_data[0]))) # clunky but checks if the job_id can be cast to int, but needs to be string after.
                except:                                          # Should be replaced with something better when refactoring.
                    pass

    def get_total_number_of_cores_in_use(self):

        total_cores_in_use = 0

        if len(self.job_ids) == 0:
            print('The length of the job_ids array is 0, make sure you have filled the array by calling get_job_ids().')
            return 
        else:
            for job_id in self.job_ids:
                total_cores_in_use += self._get_number_of_cores(job_id)

        return total_cores_in_use

    def get_all_data_of_one_job(self, job_id :str) -> dict:

        sacct_job_info = self._get_individual_job_information(job_id)

        account_name = self._get_account_name(job_id, 
                                              sacct_information_present = True, 
                                              sacct_job_info = sacct_job_info)
  
        number_of_cores = self._get_number_of_cores(job_id, 
                                                    sacct_information_present = True, 
                                                    sacct_job_info = sacct_job_info)

        partition = self._get_partition(job_id, 
                                        sacct_information_present = True, 
                                        sacct_job_info = sacct_job_info)

        account = self._get_account(job_id, 
                                    sacct_information_present = True, 
                                    sacct_job_info = sacct_job_info)
                                    
        return {'job_id' : job_id, 'number_of_cores' : number_of_cores, 'partition' : partition, 'account' : account, 'account_name' : account_name}

    def get_all_data_of_all_jobs(self) -> list:

        all_data = []
        idx = 0
        if len(self.job_ids) == 0:
            print('The length of the job_ids array is 0, make sure you have filled the array by calling get_job_ids().')
            return 
        else:
            print(f'There are currently {len(self.job_ids)} in the queue.')
            for job_id in self.job_ids:
                print(f'Working on {idx}/{len(self.job_ids)}.')
                idx += 1
                all_data.append(self.get_all_data_of_one_job(job_id))
    
        return all_data

    def _convert_string_to_number_of_minutes(self, time_string: str) -> int:
        '''
        This function takes a string in the format of 'D-HH:MM:SS' or 'HH:MM:SS' and converts it to the total number of minutes.
        The if stsatement checks if the string contains a '-' which indicates that the job has been running for more than 24 hours.
        The if statements also deal with edge cases where the string isnt as anticipated. Could be more elegant.
        '''

        split_time = time_string.split(':')

        if '-' in split_time[0]:
            days = int(split_time[0].split('-')[0])
            hours = int(split_time[0].split('-')[1])
            minutes = int(split_time[1])
            if split_time[2] == '+':
                seconds = 0
            else:
                seconds = int(split_time[2])
            return (days * 24 * 60) + (hours * 60) + minutes + (seconds /60)
        else:
            hours = int(split_time[0])
            minutes = int(split_time[1])
            seconds = int(split_time[2])
            return (hours * 60) + minutes + (seconds /60)

    def get_completed_job_information(self) -> str:
        now = datetime.now()
        time_24_hours_ago = now - timedelta(days=1)
        formatted_time_24_hours_ago = time_24_hours_ago.strftime('%Y-%m-%dT%H:%M:%S')
        return subprocess.run(['sacct', '--allusers', '--starttime', formatted_time_24_hours_ago, '--format=JobID,User,State,Elapsed,Timelimit,Partition'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def get_elapsed_time_of_jobs_over_last_24_hours(self) -> dict:
        all_job_information = self.get_completed_job_information().split('\n')

        run_times = []
        requested_times = []

        for lines in all_job_information:
            split_data = lines.split()
            if len(split_data) == 6 and split_data[2] == 'COMPLETED':
                run_time = self._convert_string_to_number_of_minutes(split_data[3])
                requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                run_times.append(run_time)
                requested_times.append(requested_time)

        return {'run_times' : run_times, 'requested_time' : requested_times}

if __name__ == '__main__':
    pass