import os
import shutil
import subprocess
import sys
import json # TODO alphabetize
import tempfile
import time
import logging

import numpy as np
import pandas as pd

import strax
import straxen

# from straxen import get_to_pe
st = straxen.contexts.strax_workshop_dali()

# TODO, go line by line on adding this back to see what the heck is going on
#SBATCH --job-name=scanner_{name}_{config}                                                             
#SBATCH --ntasks=1                                                                         
#SBATCH --cpus-per-task={n_cpu}                                                                  
#SBATCH --time={max_hours}:00:00                                                                  
#SBATCH --partition={partition}                                                                  
#SBATCH --account=pi-lgrandi                                                                    
#SBATCH --qos={partition}                                                                     
#SBATCH --output={log_fn}                                                                     
#SBATCH --error={log_fn}
# Try to make the smallest difference possible to isolate the issue.
JOB_HEADER = """#!/bin/bash
#SBATCH --job-name=strax
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --time=8:00:00
#SBATCH --partition=dali
#SBATCH --account=pi-lgrandi
#SBATCH --qos=dali

{extra_header}

# Conda
. "{conda_dir}/etc/profile.d/conda.sh"
{conda_dir}/bin/conda activate {env_name}

echo Starting jupyter job

python {python_file} {run_id} {data_path} {config_file} 
"""

# TODO, simplify defaults
def scan_parameters(strax_options=[{'run_id' : '180215_1029', 'config' : {'tail_veto_threshold' : 1e4, 
                                                                          'tail_veto_pass_fraction' : 1e3}},
                                   {'run_id' : '180215_1029', 'config' : {'dummy' : 2}},],
                    directory='/dali/lgrandi/andaloro/parameter_scan/',
                    **kwargs):
    """This is what people call

    Document this with a paragraph and parameters here.

    kwargs - max_hours, extra_header, n_cpu, mem_per_cpu
    """
    # Some checks on input

    # TODO: Check that directory exists, otherwise make it.  Use 'os'.

    # Submit each of these, such that it calls me (parameter_scan.py) with submit_setting option
    for i, strax_option in enumerate(strax_options):
        print('Submitting %d with %s' % (i, strax_option))
        submit_setting(i=i, directory=directory, **strax_option)

    pass

def make_executable(path):
    """Make the file at path executable

    TODO
    """
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def submit_setting(i, run_id, config, directory, **kwargs):
    """Docstring TODO

    More on what this does TODO.
document these variables
    """
    # This is what the script will actually execute
    print(i)
    job_fn = tempfile.NamedTemporaryFile(delete=False,
                                         dir=directory).name
    log_fn = tempfile.NamedTemporaryFile(delete=False,
                                         dir=directory).name

    config_fn = tempfile.NamedTemporaryFile(delete=False,
                                            dir=directory).name

    with open(config_fn, mode='w') as f:
        json.dump(config, f)


    # TODO: move these default settings out to above somehow.  Maybe a default dictionary
    # that gets overloaded?
    with open(job_fn, mode='w') as f:
        # Rename such that not just calling header, TODO
        # TODO PEP8
        # TODO sort these by importance or alphabetical
        f.write(JOB_HEADER.format(  
            log_fn=log_fn,
            config=str(config),
            max_hours=kwargs.get('max_hours',
                                 8),
            extra_header=kwargs.get('extra_header',
                                    ''),
            n_cpu=kwargs.get('n_cpu',
                             40),
            mem_per_cpu=kwargs.get('mem_per_cpu',
                                   4480),
            conda_dir=kwargs.get('conda_dir',
                                 '/dali/lgrandi/strax/miniconda3'),
            partition='dali',
            env_name=kwargs.get('env_name', 'strax'),
            python_file=os.path.abspath(__file__),
            config_file = config_fn,
            run_id=run_id,
            data_path='/dali/lgrandi/andaloro/strax_data', # TODO refactor this out into a variable that gets passed in.
        ))

    # Is this necessary? TODO
    make_executable(job_fn)

    print("\tSubmitting sbatch %s" % job_fn)
    result = subprocess.check_output(['sbatch', job_fn])

    print("\tsbatch returned: %s" % result)
    job_id = int(result.decode().split()[-1])

    print("\tYou have job id %d" % job_id)

def work(run_id, data_path, config):
    st = straxen.contexts.strax_workshop_dali()
    
    st.storage[-1] = strax.DataDirectory(data_path,
                                         provide_run_metadata=False)

    df = st.get_df(run_id,
                        'event_info',
                        config=config,
                        max_workers=40) # Make this 40 a variable that gets passed through TODO

    print(df.head())

 
                                          


if __name__ == "__main__":
    if len(sys.argv) == 1: # argv[0] is the filename
        print('hi I am ', __file__)
        scan_parameters()
    elif len(sys.argv) == 4:
        run_id = sys.argv[1]
        data_path = sys.argv[2]
        config_fn = sys.argv[3] # TODO: Check variable names consistent

        print(run_id, data_path, config_fn)

        with open(config_fn, mode='r') as f:
            config = json.load(f)

        work(run_id, data_path, config)
    else:
        raise ValueError("Bad command line arguments")
