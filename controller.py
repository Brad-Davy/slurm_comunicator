from slurm_comunicator import slurm_comms 

if __name__ == '__main__':
    comms = slurm_comms()
    print(comms.get_all_data_of_all_jobs())