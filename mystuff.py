from collections import OrderedDict
import numpy as np

import scanner

parameters = OrderedDict()

### EDIT BELOW TO CHANGE CONFIG SETTINGS ###

run_id = '180215_1029'
parameters['tail_veto_threshold']  = [1e4, 1e5],
parameters['tail_veto_pass_fraction'] = [0.1, 0.2]

### EDIT BELOW AT YOUR OWN RISK (OR JUST DON'T) ###

keys = list(parameters.keys())
values = list(parameters.values())

combination_values = np.array(np.meshgrid(*values)).T.reshape(-1,
                                                              len(parameters))

strax_options = []
#Enumerate over all possible options to create a strax_options list for scanning later.
for i, value in enumerate(combination_values):
    print('Setting %d:' % i)
    config = {}
    for j, parameter in enumerate(value):
          print('\t', keys[j], parameter)
          config[keys[j]] = parameter
    strax_options.append({'run_id' : run_id, 'config' : config})
    print()

print(strax_options)

#scan over everything in strax_options
scanner.scan_parameters(strax_options)
