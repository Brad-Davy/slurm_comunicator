import subprocess


class Node:
    def __init__(self, host_name: str):
        self.host_name = host_name
        self.n_cores = self.get_n_cores()

    def get_n_cores(self) -> int:
        """
        Get the number of cores available on the node.
        """
        raw_output = subprocess.run(
            ['scontrol', 'show', 'node', self.host_name]
            , stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        split_raw_output = raw_output.splitlines()
        CPUAlloc_line = [line for line in split_raw_output if 'CPUAlloc' in line]
        return int(CPUAlloc_line[0].split()[0].split('=')[1])
        
if __name__ == '__main__':
    pass