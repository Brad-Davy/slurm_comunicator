import subprocess
from datetime import datetime, timedelta
from slurm_comunicator.utils import *
import numpy as np

class Queues:
    
    def __init__(self, partition_name: str):
        self.partition_name = partition_name
        self.wait_times_list = []
        self.jobs_pending = len(self.get_current_jobs_pending())
        
    def get_current_jobs_pending(self) -> list:
        raw_job_data = subprocess.run(['squeue', 
                        f'--partition={self.partition_name}',
                        '--states=PENDING',
                        '--array', 
                        '--format=%i,%C'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

        parsed_data = []

        for lines in raw_job_data.splitlines():
            if 'JOBID' in lines:
                continue
            parsed_data.append(lines.split(','))

        return parsed_data

    def sub_start_time_difference(self, time_data: list[str]) -> int:
        '''
        Returns a float which is the difference between the start time and the submit time
        in seconds.
        '''

        if None in time_data or 'None' in time_data or 'Unknown' in time_data:
            return 0
        else:
            submit_time = datetime.strptime(time_data[1], "%Y-%m-%dT%H:%M:%S")
            start_time = datetime.strptime(time_data[2], "%Y-%m-%dT%H:%M:%S")
            wait_time = start_time - submit_time
            return convert_string_to_number_of_seconds(str(wait_time))

    def parse_time_data(self, raw_job_data: str) -> list[str]:

        parsed_data = []
        for lines in raw_job_data.splitlines():
            if 'JobID' in lines:
                continue
            parsed_data.append(lines.split('|'))

        return parsed_data


    def get_average_wait_time(self):
        raw_job_data = subprocess.run(['sacct',
                                       '--format=JobID,Submit,Start',
                                       '--starttime=now-1day',
                                       f'--partition={self.partition_name}',
                                       '--parsable2',
                                       '--allocations',
                                       '--allusers'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

        parsed_data_list = self.parse_time_data(raw_job_data)

        if len(parsed_data_list) < 1:
            return 0

        wait_times = []
        for lines in parsed_data_list:
            wait_time = self.sub_start_time_difference(lines)
            if wait_time > 0:
                wait_times.append(wait_time)
        self.wait_times_list = wait_times
        return int(np.average(wait_times) // 60)

if __name__ == '__main__':
    partition = Queues('large-long')
    print(f'Average wait time: {partition.get_average_wait_time()} minuets.')