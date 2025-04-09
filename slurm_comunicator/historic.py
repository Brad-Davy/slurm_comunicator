class HistoricComunicator:
    """
    Class to handle the communication with the historic database.
    """

    def __init__(self, db):
        """
        Initialize the HistoricCommunicator class.

        Args:
            db (Database): The database object to communicate with.
        """
        pass

    def get_completed_job_information(self) -> str:
        '''
        This function is used to get the information of all the jobs that have completed in the last 24 hours. It returns a string
        containing the information of the jobs.
        '''
        now = datetime.now()
        time_24_hours_ago = now - timedelta(days=1)
        formatted_time_24_hours_ago = time_24_hours_ago.strftime('%Y-%m-%dT%H:%M:%S')
        return subprocess.run(['sacct', '--allusers', '--starttime', formatted_time_24_hours_ago, '--format=JobID,User,State,Elapsed,Timelimit,Partition,AllocCPUS'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout


    def _is_completed_data_line_valid(self, line_data: list, partition: str) -> bool:
        if partition != '':

            if len(line_data) != 7:
                return False

            if line_data[2] != 'COMPLETED' and line_data[2] != 'CANCELLED+' and line_data[2] != 'TIMEOUT' and line_data[2] != 'FAILED':
                return False

            if line_data[5] != partition:
                return False

            return True

        else:
            if len(line_data) != 7:
                return False

            if line_data[2] != 'COMPLETED' and line_data[2] != 'CANCELLED+':
                return False

            return True


    
    def get_elapsed_time_of_jobs_over_last_24_hours(self, partition: str = '') -> dict:
        '''
        This function is used to get the elapsed time of all the jobs that have completed in the last 24 hours. It returns a
        dictionary containing the run_times and requested_times.
        '''
        all_job_information = self.get_completed_job_information().split('\n')
        run_times = []
        requested_times = []

        if partition != '':
            for lines in all_job_information:
                split_data = lines.split()
                if self._is_completed_data_line_valid(split_data, partition):
                    try:
                        run_time = self._convert_string_to_number_of_minutes(split_data[3])
                        requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                        run_times.append(run_time)
                        requested_times.append(requested_time)
                    except:
                       pass
        else:
            for lines in all_job_information:
                split_data = lines.split()
                if self._is_completed_data_line_valid(split_data, partition):
                    run_time = self._convert_string_to_number_of_minutes(split_data[3])
                    requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                    run_times.append(run_time)
                    requested_times.append(requested_time)

        return {'run_times' : run_times, 'requested_time' : requested_times}

    def elapsed_time_of_jobs_over_last_24_hours_per_partition(self) -> dict:

        all_job_information = self.get_completed_job_information().split('\n')
        partitions = {'large-long' : [[],[],[]], 'large-sho+' : [[],[],[]], 'small-long' : [[],[],[]], 'interacti+' : [[],[],[]],
                       'debug' : [[],[],[]], 'gpu' : [[],[],[]], 'small-sho+' : [[],[],[]], 'bigmem' : [[],[],[]], 'vbigmem' : [[],[],[]]}

        for lines in all_job_information:
            split_data = lines.split()

            if len(split_data) == 7 and split_data[2] == 'COMPLETED':

                partition = split_data[5]
                run_time = self._convert_string_to_number_of_minutes(split_data[3])
                requested_time = self._convert_string_to_number_of_minutes(split_data[4])
                allocated_cpus = int(split_data[6])

                if run_time > 5: # This removes job which start and fail fast, which can skew the average run time.
                    partitions[partition][0].append(run_time)
                    partitions[partition][1].append(requested_time)
                    partitions[partition][2].append(allocated_cpus)

        return partitions


if __name__ == '__main__':
    pass