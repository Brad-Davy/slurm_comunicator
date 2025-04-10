import subprocess
from slurm_comunicator.node import Node

class Partition:
    def __init__(self, name: str):
        self.name = name
        self.job_ids = []
        self.all_jobs_information = subprocess.run(
            ['squeue', '-p', self.name, '--state', 'r','--format=%i,%C']
        , stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        self.node_list = self.dertemine_node_list()
        self.number_of_cores = self.determine_n_of_cores()
        self.number_of_jobs = self.determine_n_of_jobs()
       
    def dertemine_node_list(self):
        """
        Get the list of nodes in the partition.
        """
        raw_data = subprocess.run(
            ["sinfo", "-p", self.name, "-N", "-o", "%N"], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

        split_raw_output = raw_data.splitlines()
        return [line for line in split_raw_output if 'NODELIST' not in line]

    def determine_n_of_cores(self):
        """
        Get the number of cores in the partition.
        """
        number_of_cores = 0
        for lines in self.all_jobs_information.splitlines():
            if 'JOBID' in lines:
                pass
            else:
                job_id, cores = lines.split(',')
                number_of_cores += int(cores)
        return number_of_cores

    def determine_n_of_jobs(self):
        """
        Get the number of cores in the partition.
        """
        number_of_jobs = 0
        for lines in self.all_jobs_information.splitlines():
            if 'JOBID' in lines:
                pass
            else:
                number_of_jobs += 1
        return number_of_jobs


    def calculate_to_match_with_prometheus(self) -> int:
        """
        This function is used to calculate the number of cores in the partition.
        It returns a dictionary containing the partition name and the number of cores.
        """
        number_of_cores = 0
        for node in self.node_list:
            node = Node(node)
            number_of_cores += node.n_cores
        return number_of_cores


if __name__ == '__main__':
    pass
