from slurm_comunicator import slurm_comms 
import pandas as pd

if __name__ == '__main__':
    comms = slurm_comms()
    data = comms.get_all_data_of_all_jobs()
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)