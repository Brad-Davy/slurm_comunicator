import subprocess
from datetime import datetime, timedelta
from tqdm import tqdm
from slurm_comunicator.utils import *
from slurm_comunicator.partitions import Partition
from slurm_comunicator.historic_parition import HistoricPartition
import line_profiler
import threading 

class SlurmComms:
    '''
    This class is used to communicate with the slurm scheduler on the HPC. It can be used to get information on the number 
    of cores being used, the number of jobs in the queue, the number of jobs that have completed in the last 24 hours and 
    the average run time of a job over the last 24 hours.
    '''

    def __init__(self, prometheus_comparison: bool = False):
        self.prometheus_comparison = prometheus_comparison
        self.partitions = self.get_partitions()

        def fetch_historic_data():
            for partitions in self.partitions:
                h_partition = HistoricPartition(partitions)
                manage_partition_csv_file(h_partition.name, {'run_times': h_partition.run_times, 'requested_times': h_partition.requested_times})

        thread_historic_data = threading.Thread(target=fetch_historic_data)
        thread_historic_data.start()

        self.total_cores_in_use = self.get_total_cores_in_use()
        self.total_cores_in_cluster = self.get_total_cores_in_cluster()
        self.n_running_jobs_in_queue = self.get_n_running_jobs_in_queue()
        self.n_pending_jobs_in_queue = self.get_n_pending_jobs_in_queue()
        thread_historic_data.join()

    def __str__(self):
        return f'Partitions: {self.partitions}'

    def get_partitions(self) -> list:
        '''
        This function is used to get the partitions on the HPC. It returns a list of partitions.
        '''
        raw_data = subprocess.run(['sinfo', '-o', '%P'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        split_raw_output = raw_data.splitlines()
        return [line for line in split_raw_output if 'PARTITION' not in line]

    def get_total_cores_in_use(self) -> int:
        '''
        This function is used to get the total number of cores in use on the HPC. It returns the total number of cores.
        '''
        number_of_cores = 0
        for partition in self.partitions:
            parition = Partition(partition, self.prometheus_comparison)
            number_of_cores += parition.number_of_cores

        return number_of_cores

    def get_total_cores_in_cluster(self) -> int:
        '''
        This function is used to get the total number of cores in the cluster. It returns the total number of cores.
        '''
        raw_data = subprocess.run(['sinfo', '-o', '%C'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        split_raw_output = raw_data.splitlines()
        return int(split_raw_output[1].split('/')[-1])

    def get_n_running_jobs_in_queue(self) -> int:
        return len(subprocess.run(['squeue', '--state', 'r','-o', '%i'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.splitlines()) -1
    
    def get_n_pending_jobs_in_queue(self) -> int:
        return len(subprocess.run(['squeue', '--state', 'PD','-o', '%i'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.splitlines()) -1
    
    def get_n_cores_partition_dictionary(self) -> dict:
        '''
        This function is used to get the number of cores in each partition. 
        It returns a dictionary containing the partition name
        and the number of cores.
        '''
        partition_dictionary = {}
        for partition in self.partitions:
            partition = Partition(partition, self.prometheus_comparison)
            partition_dictionary[partition.name] = partition.number_of_cores
        return partition_dictionary
   
    def get_n_jobs_partition_dictionary(self) -> dict:
        '''
        This function is used to get the number of jobs in each partition. 
        It returns a dictionary containing the partition name
        '''
        partition_dictionary = {}
        for partition in self.partitions:
            partition = Partition(partition)
            partition_dictionary[partition.name] = partition.number_of_jobs
        return partition_dictionary

    def get_average_wait_time_partition_dictionary(self) -> dict:

        partition_dictionary = {}
        for partition in self.partitions:
            partition = Partition(partition)
            partition_dictionary[partition.name] = partition.average_wait_time
        return partition_dictionary

    def get_queue_length_partition_dictionary(self) -> dict:

        partition_dictionary = {}
        for partition in self.partitions:
            partition = Partition(partition)
            partition_dictionary[partition.name] = partition.jobs_pending
        return partition_dictionary

if __name__ == '__main__':
    comms = SlurmComms()
    print(comms.get_average_wait_time_partition_dictionary())


