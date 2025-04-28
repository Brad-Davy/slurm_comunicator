import pandas as pd
from datetime import date
import numpy as np
import os 


def manage_partition_csv_file(partition_name: str, partition_data: dict) -> None:

    file_path = f'/home/bd67/.hypatia_logs/partitions/{partition_name}'

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    create_csv_file(partition_data, f'{file_path}/{partition_name}_{date.today()}.csv')

def manage_csv_file(data: dict, file_name: str) -> None:


    file_path = f'/home/bd67/.hypatia_logs/{file_name.split('-')[0]}'

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    create_csv_file(data, file_path+f'/{file_name}')

def create_csv_file(data: dict, csv_file_path: str) -> None:
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)

def append_csv_file(data: dict, csv_file_path: str) -> None:
    df = pd.DataFrame(data)
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

def convert_string_to_number_of_minutes(time_string: str) -> int:
    '''
    This function takes a string in the format of 'D-HH:MM:SS' or 'HH:MM:SS' and converts it to the total number of minutes.
    The if stsatement checks if the string contains a '-' which indicates that the job has been running for more than 24 hours.
    The if statements also deal with edge cases where the string isnt as anticipated. Could be more elegant.
    '''

    split_time = time_string.split(':')

    if '-' in split_time[0]:
        days = int(split_time[0].split('-')[0])
        hours = int(split_time[0].split('-')[1])
        minutes = int(split_time[1])
        if split_time[2] == '+':
            seconds = 0
        else:
            seconds = int(split_time[2])
        return (days * 24 * 60) + (hours * 60) + minutes + (seconds /60)
    else:
        try:
            hours = int(split_time[0])
            minutes = int(split_time[1])
            seconds = int(split_time[2])
            return (hours * 60) + minutes + (seconds /60)
        except:
            return 0

def convert_string_to_number_of_seconds(time_string: str) -> int:
    '''
    This function takes a string in the format of 'D-HH:MM:SS' or 'HH:MM:SS' and converts it to the total number of minutes.
    The if stsatement checks if the string contains a '-' which indicates that the job has been running for more than 24 hours.
    The if statements also deal with edge cases where the string isnt as anticipated. Could be more elegant.
    '''

    split_time = time_string.split(':')

    if '-' in split_time[0]:
        days = int(split_time[0].split('-')[0])
        hours = int(split_time[0].split('-')[1])
        minutes = int(split_time[1])
        if split_time[2] == '+':
            seconds = 0
        else:
            seconds = int(split_time[2])
        return (days * 24 * 60 * 60) + (hours * 60 * 60) + minutes + seconds
    else:
        try:
            hours = int(split_time[0])
            minutes = int(split_time[1])
            seconds = int(split_time[2])
            return (hours * 60 * 60) + minutes*60 + seconds
        except:
            return 0



if __name__ == '__main__':
    pass
