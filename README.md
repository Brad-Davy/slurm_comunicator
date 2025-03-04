# SLURM Communicator

## Overview
SLURM Communicator is a tool designed to facilitate communication with the SLURM workload manager. It provides an easy-to-use interface for submitting, monitoring, and managing jobs on a SLURM cluster.

## Features
- Determine how many cores are currently in use.
- Determine how long jobs are running for and how much time is being requested.

## Installation
To install SLURM Communicator, clone the repository and install the required dependencies:
```bash
git clone https://github.com/yourusername/slurm_communicator.git
cd slurm_communicator
pip install -r requirements.txt
```

## Usage
To use SLURM Communicator, run the main script with the appropriate commands:
```bash
python slurm_communicator.py [command] [options]
```

### Example
Submit a job to the SLURM scheduler:
```bash
python slurm_communicator.py submit --script job_script.sh
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please open an issue on the GitHub repository or contact the maintainer at your.email@example.com.