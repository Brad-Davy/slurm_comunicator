from slurm_comunicator import slurm_comms 
from utils import *

if __name__ == '__main__':
    comms = slurm_comms()
    save_array_as_excel(comms.get_all_data_of_all_jobs(), 'output')