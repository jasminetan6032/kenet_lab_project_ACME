from os.path import join
from numpy import arange
from multiprocessing import cpu_count
from time import strftime

### TOP LEVEL ### variables, locations independent of paradigm
current_datetime = strftime('%Y%m%d-%H%M%S')

transcend_dir = '/autofs/cluster/transcend'

meg_dir = join(transcend_dir, 'MEG') # MEG directory
erm_dir = join(meg_dir, 'erm') # MEG empty room recordings directory

subjects_dir = join(transcend_dir, 'MRI', 'WMA', 'recons') # MRI directory - recons directory - FreeSurfer notation

shared_func_dir = join(transcend_dir, 'scripts')

n_jobs = max(cpu_count() - 4, 1)

### MID LEVEL ### paradigm-relevant parameters, variables...
paradigm = 'ASSRnew_Jumps'
paradigm_dir = join(meg_dir, paradigm)
paradigm_vars_output_filename = f'{paradigm}_paradigm_config_variables_output_{current_datetime}.txt'

reports_dir = join(paradigm_dir, 'reports')


# noise covariance matrix, inverse computation done by using either baseline period or ERM
proc_using_baseline = False
proc_using_erm = False if proc_using_baseline else True

### LOW LEVEL ### analysis-relevant parameters, variables, etc...
# bandpass filtering
l_freq = 0.1
h_freq = 144.

# merged/specified/grouped event IDs, conditions
# key <-> condition name
# value <-> condition's information (nested dictionary)
conditions_dicts = {'Jump': {'event_id': [1, 2, 3, 4]},
                    'NoJump': {'event_id': [5, 6, 7, 8, 9, 10, 11, 12]},
                    'Jump25Hz': {'event_id': [1, 3]},
                    'Jump43Hz': {'event_id': [2, 4]},
                    'NoJump25Hz': {'event_id': [5, 7, 9, 11]},
                    'NoJump43Hz': {'event_id': [6, 8, 10, 12]},
                    'L2R': {'event_id': [1, 2]},
                    'R2L': {'event_id': [3, 4]},
                    'L2L': {'event_id': [5, 6, 9, 10]},
                    'R2R': {'event_id': [7, 8, 11, 12]}}



# artifact removal method(s)
preproc_ssp = True
preproc_ica = False if preproc_ssp else True # eventually add infrastructure to handle both methods simultaneously

# epoching parameters
epoch_tmin = -0.3
epoch_tmax = 2.

epoch_dur = (epoch_tmax - epoch_tmin) * 1000.
epoch_baseline = (epoch_tmin, 0.)
epoch_proj = True if preproc_ssp else False

grad_epoch_reject = 5000e-13
mag_epoch_reject = 4e-12
eeg_epoch_reject = 500e-6

epoch_reject = dict(grad=grad_epoch_reject, mag=mag_epoch_reject, eeg=eeg_epoch_reject)

epochs_parameters_dict = {'tmin': epoch_tmin, 'tmax': epoch_tmax,
                          'baseline': epoch_baseline, 'proj': epoch_proj,
                          'reject': None}

# parameters dictionary for windowing power/ITC, include modes like 'mean', 'max'...
freqs = arange(15, 50, 2) # frequencies of interest
n_cycles = freqs / 2.  # different number of cycles per frequency
n_cycles[freqs < 15] = 2

# sensor power/ITC windowing parameters
tfr_t_start = 0.1
tfr_t_end = 0.9
tfr_temporal_dict = {'t_start':tfr_t_start, 't_end': tfr_t_end}

sensor_report_fname = f'sensor_space_{paradigm}_{current_datetime}_report.h5' # sensor space report filename

with open(join(paradigm_dir, paradigm_vars_output_filename), 'w+') as var_output:
    for var_name, value in dict(vars()).items():
        var_output.write(f'{var_name}: {value}\n')
var_output.close()
