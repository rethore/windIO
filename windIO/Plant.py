# License: Apache 2.0
# Author: Pierre-Elouan Rethore
# Email: pire@dtu.dk
#

import yaml
import numpy as np

class WTLayout(object):
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as f:
            data = yaml.load(f)
        self.wt_names = list(data['turbines'].keys())
        self.wt_names.sort()
        self.data = data
        self.check_structure(data)

    def __getitem__(self, a):
        return self.data[a]

    def __setitem__(self, a, b):
        self.data[a] = b

    @property
    def wt_list(self):
        return [self.data['turbines'][wtn] for wtn in self.wt_names]

    @property
    def positions(self):
        return np.array([wt['position'] for wt in self.wt_list])

    def check_structure(self, data):
        base = ['turbines', 'turbine_types']
        for k, v in data.items():
            if not k in base:
                raise KeyError('key: {0} not recognized'.format(k))

        # Check for all turbines to have a defined type
        for k, v in data['turbines'].items():
            if 'type' in v:
                if not v['type'] in data['turbine_types']:
                    raise Exception("turbine: {0} type: {1} is not defined in `turbine_types`".format(k, v['type']))
            else:
                raise KeyError("turbine: {0} doesn't have a defined type".format(k))

        # Check that the turbines have a position
        for k, v in data['turbines'].items():
            if 'position' not in v:
                raise Exception("turbine: {0} doesn't have a defined position".format(k))
