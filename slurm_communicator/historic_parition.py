from datetime import datetime, timedelta
import subprocess


class HistoricPartition:
    def __init__(self, name: str):
        self.name = name
        self.run_times, self.requested_times = self.get_average_run_times()

    def _get_completed_job_information(self) -> str:
        """
        This function is used to get the information of all the jobs that have completed in the last 24 hours. It returns a string
        containing the information of the jobs.
        """
        now = datetime.now()
        time_24_hours_ago = now - timedelta(days=1)
        formatted_time_24_hours_ago = time_24_hours_ago.strftime("%Y-%m-%dT%H:%M:%S")
        return subprocess.run(
            [
                "sacct",
                "--allusers",
                "--starttime",
                formatted_time_24_hours_ago,
                "--partition",
                self.name,
                "--format=State,Elapsed,Timelimit,AllocCPUS",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout

    def _is_completed_data_line_valid(self, line_data: list) -> bool:

        if len(line_data) != 4:
            return False

        if (
            line_data[0] != "COMPLETED"
            and line_data[0] != "CANCELLED+"
            and line_data[0] != "TIMEOUT"
            and line_data[0] != "FAILED"
        ):
            return False

        return True

    def get_average_run_times(self) -> tuple[list[float], list[float]]:
        run_times = []
        requested_times = []

        for lines in self._get_completed_job_information().split("\n"):
            split_data = lines.split()

            if self._is_completed_data_line_valid(split_data):
                run_times.append(split_data[1])
                requested_times.append(split_data[2])

        return (run_times, requested_times)


if __name__ == "__main__":
    partition = HistoricPartition("large-long")
    print(partition.run_times)
    print(partition.requested_times)
    manage_csv_file(
        parition.name,
        {
            "run_times": partition.run_times,
            "requested_times": partition.requested_times,
        },
    )
