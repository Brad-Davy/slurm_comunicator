from slurm_comunicator import slurm_comms 
import pandas as pd
from datetime import date

def save_array_as_excel(input_array: list, file_name: str = 'output') -> None:
    df = pd.DataFrame(input_array)
    df.to_excel(f'{file_name}_{date.today()}.xlsx', index=False)

if __name__ == '__main__':
    pass