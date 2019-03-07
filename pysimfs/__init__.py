#! /usr/bin/env python

from collections import namedtuple
import os

import numpy as np

basepath = '/opt/SiMFS-Tk/SiMFS-core/build/src/components/' # Make configurable

def find_component(comp: str, directory: str) -> bool:
    return os.path.exists(os.path.join(basepath, directory, comp)) 


for comp in ['simfs_dif', 'simfs_sft', 'simfs_cnf']:
    assert find_component(comp, 'mol'), f'mol/{comp} not found in {basepath}'

for comp in ['simfs_exi', 'simfs_det', 'simfs_pre', 'simfs_pls']:
    assert find_component(comp, 'fcs'), f'fcs/{comp} not found in {basepath}'
    
for comp in ['simfs_ph2']:
    assert find_component(comp, 'ph2'), f'ph2/{comp} not found in {basepath}'

for comp in ['simfs_buf', 'simfs_spl', 'simfs_mix', 'simfs_img']:
    assert find_component(comp, 'utl'), f'utl/{comp} not found in {basepath}'

print(f'All simfs components found in {basepath}.')

IO = namedtuple('IO', ['name', 'dtype'])
ComponentLog = namedtuple('ComponentLog', ['params', 'error'])

coordinate_t = np.dtype([('x', 'f8'), ('y', 'f8'),('z', 'f8'), ('t', 'f8')])
timed_value_t = np.dtype([('v', 'f8'), ('t', 'f8')])
timetag_t = np.dtype('f8')

from . component import *
from . presets import *
from . import mocks
from . import utils

try:
    ip = get_ipython()
    ip.register_magics(SimfsDefaultMagics)
except NameError:
    pass # ipython not found

