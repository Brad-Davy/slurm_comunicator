import os
import subprocess

class slurm_comms:

    def __init__(self):
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        self.job_ids = []
        self.fill_job_ids_array()


    def _get_current_job_information(self):
        self.all_jobs_information = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def _get_number_of_cores(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> int:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 7:
            return int(split_job_information[4])
        elif len(split_job_information) == 8:
            return int(split_job_information[5])

    def _get_partition(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 7:
            return str(split_job_information[2])
        elif len(split_job_information) == 8:
            return str(split_job_information[3])

    def _get_account(self, job_id: str, sacct_information_present: bool = False, sacct_job_info: str = '') -> str:

        if sacct_information_present == False:
            sacct_job_info = self._get_individual_job_information(job_id)
        
        split_job_information = sacct_job_info.split('\n')[2].split()

        if len(split_job_information) == 7:
            return str(split_job_information[3])
        elif len(split_job_information) == 8:
            return str(split_job_information[4])

    def _get_individual_job_information(self, job_id: str) -> str:
        return subprocess.run(['sacct', '-j', job_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    def fill_job_ids_array(self):

        for lines in self.all_jobs_information.split('\n'):
            split_data = lines.split()
            if len(split_data) == 8:
                try:
                    self.job_ids.append(str(int(split_data[0]))) # clunky but checks if the job_id can be cast to int, but needs to be string afer.
                except:
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

    def get_all_data(self, job_id :str) -> list:

        sacct_job_info = self._get_individual_job_information(job_id)
        number_of_cores = self._get_number_of_cores(job_id, sacct_information_present = True, sacct_job_info = sacct_job_info) 
        partition = self._get_partition(job_id, sacct_information_present = True, sacct_job_info = sacct_job_info)
        account = self._get_account(job_id, sacct_information_present = True, sacct_job_info = sacct_job_info)
        return [number_of_cores, partition, account]

if __name__ == '__main__':
    coms = slurm_comms()
    total_cores_used = coms.get_total_number_of_cores_in_use()
    print(f'Total cores used: {total_cores_used}, {100*(total_cores_used/15102):.2f}% of the HPC is currently being used.')