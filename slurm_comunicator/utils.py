import pandas as pd
from datetime import date
import numpy as np

def create_csv_file(data: dict, file_name: str = 'slurm_comunicator.csv') -> None:
    csv_file_path = f'/home/bd67/scratch/hypatia_logs/{file_name}'
    df = pd.DataFrame(data, index=[0])
    df.to_csv(csv_file_path, index=False)

def append_csv_file(input_data: dict, file_name: str) -> None:
    csv_file_path = f'/home/bd67/scratch/hypatia_logs/{file_name}'
    df = pd.DataFrame(input_data, index=[0])
    df.to_csv(csv_file_path, mode='a', header=False, index=False)

def print_csv_file(file_names: list[str]) -> None:
    for file_name in file_names:
        csv_file_path = f'/home/bd67/scratch/hypatia_logs/{file_name}'
        
        try:
            df = pd.read_csv(csv_file_path, on_bad_lines="skip", engine="python")  # Skip bad lines
            print(df)
        except pd.errors.ParserError as e:
            print(f"Error parsing {file_name}: {e}")
        except FileNotFoundError:
            print(f"File not found: {csv_file_path}")

def save_array_as_excel(input_array: list, file_name: str = 'output') -> None:
    df = pd.DataFrame(input_array)
    df.to_excel(f'xlsx/{file_name}_{date.today()}.xlsx', index=False)

def convert_minuets_in_to_time_string(minutes: int) -> str:
    try:
        if int(minutes // 60) < 24:
            hours = int(minutes // 60)
            minutes = int(minutes % 60)
            return f'{hours}:{minutes}'
        else:
            days = int(minutes // 1440)
            hours = int((minutes % 1440) // 60)
            minutes = int((minutes % 1440) % 60)
            return f'{days}-{hours}:{minutes}'
    except:
        print(minutes)
        return '0:0'
        
if __name__ == '__main__':
    pass
