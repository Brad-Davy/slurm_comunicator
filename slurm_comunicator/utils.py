from slurm_comunicator.slurm_comunicator import SlurmComms
import pandas as pd
from datetime import date

def save_array_as_excel(input_array: list, file_name: str = 'output') -> None:
    df = pd.DataFrame(input_array)
    df.to_excel(f'{file_name}_{date.today()}.xlsx', index=False)

def convert_minuets_in_to_time_string(minutes: int) -> str:
    if int(minutes // 60) < 24:
        hours = int(minutes // 60)
        minutes = int(minutes % 60)
        return f'{hours}:{minutes}'
    else:
        days = int(minutes // 1440)
        hours = int((minutes % 1440) // 60)
        minutes = int((minutes % 1440) % 60)
        return f'{days}-{hours}:{minutes}'
        
if __name__ == '__main__':
    pass