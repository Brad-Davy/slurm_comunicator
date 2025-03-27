import subprocess
from datetime import datetime, timedelta
from tqdm import tqdm
from slurm_comunicator.utils import *

class SlurmComms:
    '''
    This class is used to communicate with the slurm scheduler on the HPC. It can be used to get information on the number 
    of cores being used, the number of jobs in the queue, the number of jobs that have completed in the last 24 hours and 
    the average run time of a job over the last 24 hours.
    '''

    def __init__(self):
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        self.job_ids = []
        self.job_data = []
        self.fill_job_ids_array()


    def _get_current_job_information(self):
        '''
        This function is used to get the current job information from the slurm scheduler. It is called in the __init__ function.
        '''
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def _get_number_of_cores(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> int:
        '''
        This function is used to get the number of cores that a job is using. It takes a job_id as an argument and returns 
        the number of cores. The sacct_information_present argument is used to check if the information has already been 
        retrieved, if it has then the function does not need to call the sacct command again. This is useful when calling 
        this function multiple times in a loop.
        '''

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)

        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 5:
            return int(split_job_information[2])
        else:
            return 0 # quick fix for now, should add a bool arg which returns false if respone isnt valid (i.e. len() != 4).

    def _get_partition(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:
        '''
        This function is used to get the partition that a job is running on. It takes a job_id as an argument and returns
        the partition. The sacct_information_present argument is used to check if the information has already been
        retrieved, if it has then the function does not need to call the sacct command again. This is useful when calling
        this function multiple times in a loop.
        '''

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)

        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 5:
            return str(split_job_information[3])
        else:
            return ''

    def _get_state(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:
        '''
        This function is used to get the partition that a job is running on. It takes a job_id as an argument and returns
        the partition. The sacct_information_present argument is used to check if the information has already been
        retrieved, if it has then the function does not need to call the sacct command again. This is useful when calling
        this function multiple times in a loop.
        '''

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)

        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 5:
            return str(split_job_information[-1])
        else:
            return ''

    def _get_account(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:
        '''
        This function is used to get the account that a job is running on. It takes a job_id as an argument and returns
        the account. The sacct_information_present argument is used to check if the information has already been
        retrieved, if it has then the function does not need to call the sacct command again. This is useful when calling
        this function multiple times in a loop.
        '''

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)

        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 5:
            return str(split_job_information[2])
        else:
            return ''

    def _get_account_name(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:
        '''
        This function is used to get the account name that a job is running on. It takes a job_id as an argument and returns
        the account name. The sacct_information_present argument is used to check if the information has already been
        retrieved, if it has then the function does not need to call the sacct command again. This is useful when calling
        this function multiple times in a loop.
        '''

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 5:
            return str(split_job_information[0])
        else:
            return ''

    def _get_individual_job_information(self, job_id: str) -> str:
        '''
        This function is used to get the information of a single job. It takes a job_id as an argument and returns the
        information of that job.
        '''
        return subprocess.run(['sacct', '-j', job_id, '--format=User,Account,AllocCPUS,Partition,State'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def line_data_is_okay(self, line_data):

        split_line_data = line_data.split()

        if len(split_line_data) == 9:
            return True, split_line_data[0]

        if len(split_line_data) != 8:
            return False, ''

        if '_' in split_line_data[0]:
            return False, ''

        if split_line_data[0] == 'JOBID':
            return False, ''

        return True, split_line_data[0]



    def fill_job_ids_array(self):
        '''
        This function is used to fill the job_ids array with the job_ids of all the jobs in the queue. 
        It is called in the __init__ function.
        '''

        for lines in self.all_jobs_information.split('\n'):

            add_data, job = self.line_data_is_okay(lines)
            if add_data:
                self.job_ids.append(job)

    def get_total_number_of_cores_in_use(self):
        '''
        This function is used to get the total number of cores being used on the HPC. It returns the total number of cores.
        '''

        total_cores_in_use = 0

        if len(self.job_ids) == 0:
            print('The length of the job_ids array is 0, make sure you have filled the array by calling get_job_ids().')
            return 
        else:
            for job_id in self.job_ids:
                total_cores_in_use += self._get_number_of_cores(job_id)

        return total_cores_in_use

    def get_all_data_of_one_job(self, job_id :str) -> dict:
        '''
        This function is used to get all the information of a single job. It takes a job_id as an argument and returns a
        dictionary containing the job_id, number_of_cores, partition, account and account_name.
        '''

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
        '''
        This function is used to get the information of all the jobs that have completed in the last 24 hours. It returns a string
        containing the information of the jobs.
        '''
        now = datetime.now()
        time_24_hours_ago = now - timedelta(days=1)
        formatted_time_24_hours_ago = time_24_hours_ago.strftime('%Y-%m-%dT%H:%M:%S')
        return subprocess.run(['sacct', '--allusers', '--starttime', formatted_time_24_hours_ago, '--format=JobID,User,State,Elapsed,Timelimit,Partition,AllocCPUS'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout


    def _is_completed_data_line_valid(self, line_data: list, partition: str) -> bool:

        if partition != '':

            if len(line_data) != 7:
                return False

            if line_data[2] != 'COMPLETED' and line_data[2] != 'CANCELLED+' and line_data[2] != 'TIMEOUT' and line_data[2] != 'FAILED':
                return False

            if line_data[5] != partition:
                return False

            return True

        else:
            if len(line_data) != 7:
                return False

            if line_data[2] != 'COMPLETED' and line_data[2] != 'CANCELLED+':
                return False

            return True


    def get_elapsed_time_of_jobs_over_last_24_hours(self, partition: str = '') -> dict:
        '''
        This function is used to get the elapsed time of all the jobs that have completed in the last 24 hours. It returns a
        dictionary containing the run_times and requested_times.
        '''
        all_job_information = self.get_completed_job_information().split('\n')
        run_times = []
        requested_times = []

        if partition != '':
            for lines in all_job_information:
                split_data = lines.split()
                if self._is_completed_data_line_valid(split_data, partition):

                    run_time = self._convert_string_to_number_of_minutes(split_data[3])
                    requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                    run_times.append(run_time)
                    requested_times.append(requested_time)
        else:
            for lines in all_job_information:
                split_data = lines.split()
                if self._is_completed_data_line_valid(split_data, partition):
                    run_time = self._convert_string_to_number_of_minutes(split_data[3])
                    requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                    run_times.append(run_time)
                    requested_times.append(requested_time)

        return {'run_times' : run_times, 'requested_time' : requested_times}
    
    def elapsed_time_of_jobs_over_last_24_hours_per_partition(self) -> dict:

        all_job_information = self.get_completed_job_information().split('\n')
        partitions = {'large-long' : [[],[],[]], 'large-sho+' : [[],[],[]], 'small-long' : [[],[],[]], 'interacti+' : [[],[],[]],
                       'debug' : [[],[],[]], 'gpu' : [[],[],[]], 'small-sho+' : [[],[],[]], 'bigmem' : [[],[],[]], 'vbigmem' : [[],[],[]]}

        for lines in all_job_information:
            split_data = lines.split()

            if len(split_data) == 7 and split_data[2] == 'COMPLETED':

                partition = split_data[5]
                run_time = self._convert_string_to_number_of_minutes(split_data[3])
                requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                allocated_cpus = int(split_data[6])

                if run_time > 5: # This removes job which start and fail fast, which can skew the average run time.
                    partitions[partition][0].append(run_time)
                    partitions[partition][1].append(requested_time)
                    partitions[partition][2].append(allocated_cpus)

        return partitions
    
    def get_all_data_of_all_jobs(self) -> list:
        '''
        This function is used to get all the information of all the jobs in the queue. It returns a list of dictionaries
        containing the job_id, number_of_cores, partition, account and account_name.
        '''

        all_data = []
        idx = 0
        if len(self.job_ids) == 0:
            print('The length of the job_ids array is 0, make sure you have filled the array by calling get_job_ids().')
            return
        else:
            print(f'There are currently {len(self.job_ids)} jobs in the queue. Checking each job now.')
            print('\n')
            for job_id in tqdm(self.job_ids):
                idx += 1
                all_data.append(self.get_all_data_of_one_job(job_id))

        return all_data

    def get_all_partition_data(self):

        job_partitions = {}
        print('1032774' in self.job_ids)
        for job_id in self.job_ids:
            parition = self._get_partition(job_id)
            if parition in job_partitions:
                job_partitions[parition].append(job_id)
            else:
                job_partitions[parition] = [job_id]

        return job_partitions

if __name__ == '__main__':
    pass
