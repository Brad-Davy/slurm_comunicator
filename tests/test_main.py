from slurm_comunicator.comunicator import SlurmComms
from slurm_comunicator.utils import *
import subprocess


## Tests SlurmComms class ##
def test_partition_cores_equals_total_cores():
    comms = SlurmComms()
    assert (
        sum(comms.get_n_cores_partition_dictionary().values())
        == comms.get_total_cores_in_use()
    )
