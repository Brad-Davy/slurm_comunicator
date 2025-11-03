import subprocess
from datetime import datetime
from slurm_comunicator.utils import *
import numpy as np


class Queues:
    """
    A class for gathering and analysing job queue information for a specific SLURM partition.

    Attributes:
        partition_name (str): The name of the partition to monitor.
        wait_times_list (list): List of wait times for jobs.
        jobs_pending (int): Number of jobs currently pending.
    """

    def __init__(self, partition_name: str):
        """
        Initializes the Queues object.

        Args:
            partition_name (str): The SLURM partition name to analyse.
        """
        self.partition_name = partition_name
        self.wait_times_list = []
        self.jobs_pending = len(self.get_current_jobs_pending())

    def get_current_jobs_pending(self) -> list:
        """
        Retrieves the list of currently pending jobs in the specified partition.

        Returns:
            list: A list of [JobID, CPUs] for pending jobs.
        """
        raw_job_data = subprocess.run(
            [
                "squeue",
                f"--partition={self.partition_name}",
                "--states=PENDING",
                "--array",
                "--format=%i,%C",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout

        parsed_data = []

        for lines in raw_job_data.splitlines():
            if "JOBID" in lines:
                continue
            parsed_data.append(lines.split(","))

        return parsed_data

    def sub_start_time_difference(self, time_data: list[str]) -> int:
        """
        Calculates the wait time in seconds between job submission and job start.

        Args:
            time_data (list[str]): A list containing [JobID, SubmitTime, StartTime].

        Returns:
            int: Wait time in seconds, or 0 if time is not available.
        """
        if None in time_data or "None" in time_data or "Unknown" in time_data:
            return 0
        else:
            submit_time = datetime.strptime(time_data[1], "%Y-%m-%dT%H:%M:%S")
            start_time = datetime.strptime(time_data[2], "%Y-%m-%dT%H:%M:%S")
            wait_time = start_time - submit_time
            return convert_string_to_number_of_seconds(str(wait_time))

    def parse_time_data(self, raw_job_data: str) -> list[str]:
        """
        Parses raw job time data into a list of values.

        Args:
            raw_job_data (str): Output from `sacct` command in pipe-separated format.

        Returns:
            list[str]: Parsed list of job timing info.
        """
        parsed_data = []
        for lines in raw_job_data.splitlines():
            if "JobID" in lines:
                continue
            parsed_data.append(lines.split("|"))

        return parsed_data

    def determine_users(self) -> dict:
        """
        Determines a dictionary of users which have submitted jobs.

        Returns:
            dict:{user : n_jobs}
        """
        raw_job_data = subprocess.run(
            [
                "sacct",
                "--format=User",
                "--starttime=now-1day",
                f"--partition={self.partition_name}",
                "--parsable2",
                "--allocations",
                "--allusers",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout
        user_dict = {}
        for lines in raw_job_data.splitlines():

            if lines == "User":
                continue

            else:
                if lines in user_dict:
                    user_dict[lines] += 1
                else:
                    user_dict[lines] = 1
        return user_dict

    def get_average_wait_time(self) -> int:
        """
        Computes the average wait time for jobs submitted in the last 24 hours.

        Returns:
            int: Average wait time in minutes.
        """
        raw_job_data = subprocess.run(
            [
                "sacct",
                "--format=JobID,Submit,Start",
                "--starttime=now-1day",
                f"--partition={self.partition_name}",
                "--parsable2",
                "--allocations",
                "--allusers",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout

        parsed_data_list = self.parse_time_data(raw_job_data)

        if len(parsed_data_list) < 1:
            return 0

        wait_times = []
        for lines in parsed_data_list:
            wait_time = self.sub_start_time_difference(lines)
            if wait_time > 0:
                wait_times.append(wait_time)
        self.wait_times_list = wait_times
        if len(wait_times) > 0:
            return int(np.average(wait_times) // 60)
        else:
            return 0


if __name__ == "__main__":
    partition = Queues("large-short")
    print(f"Average wait time: {partition.get_average_wait_time()} minutes.")
    print(partition.determine_users())
