import subprocess
from slurm_comunicator.node import Node

class Partition:
    def __init__(self, name: str):
        self.name = name
        self.number_of_cores = self.determine_n_of_cores()
        self.job_ids = []
        self.all_jobs_information = subprocess.run(
            ['squeue', '-p', self.name, '--state', 'r','--format=%i,%C']
        , stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        self.node_list = self.dertemine_node_list()
        self.avg_job_length = self.determine_avg_job_length()
       
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

    def determine_avg_job_length(self):
        """
        Get the average job length in the partition.
        """
        pass


if __name__ == '__main__':
    partition = Partition("large-long")
    partition.determine_n_of_cores()
    print(f'Number of cores according to partition:{partition.number_of_cores}')
    number_of_cores = 0
    for lines in partition.node_list:
        node = Node(lines)
        number_of_cores += node.n_cores
    print(f'Number of cores according to nodes:{number_of_cores}')
