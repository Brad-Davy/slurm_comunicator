from slurm_comunicator import slurm_comms 

if __name__ == '__main__':
    comms = slurm_comms()
    #total_cores_used = comms.get_total_number_of_cores_in_use()
    #print(f'Total cores used: {total_cores_used}, {100*(total_cores_used/15102):.2f}% of the HPC is currently being used.')

    print(comms._get_number_of_cores('1013925'))
    print(comms.get_all_data('1013925'))