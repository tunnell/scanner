import numpy as np
from collections import OrderedDict

import scanner

parameters = OrderedDict()

# EDIT HERE
run_id = '180215_1029'
parameters['tail_veto_threshold']  = [1e4, 1e5],
parameters['tail_veto_pass_fraction'] = [0.1, 0.2]

# DO NOT EDIT BELOW

keys = list(parameters.keys())
values = list(parameters.values())

combination_values = np.array(np.meshgrid(*values)).T.reshape(-1,
                                                              len(parameters))

strax_options = []
for i, value in enumerate(combination_values):
    print('Setting %d:' % i)
    config = {}
    for j, parameter in enumerate(value):
          print('\t', keys[j], parameter)
          config[keys[j]] = parameter
    strax_options.append({'run_id' : run_id, 'config' : config})
    print()

print(strax_options)

scanner.scan_parameters(strax_options)




