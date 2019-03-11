###############################################################################
###############################################################################
###############################################################################

from . import IO, coordinate_t, timed_value_t, timetag_t, cmp_dir
from . pysimfs import Simulation 

import json
import os
import uuid

class Component:

    input_paths = []
    output_paths = []
    opts = []
    cmd = ''

    ########################################################################### 
    def __init__(self, name=None, **params):

        self.call = os.path.join(cmp_dir, self.cmd)
        self.name = f'{self.cmd}:{str(uuid.uuid1())[:8]}'

        if name:
            self.name = ':'.join((name, self.name))

        self.params= params
        self._params = params
        self.validate_params()

    @property
    def all_params(self):
        return self._params


    def validate_params(self):
        '''Pass configured params to simfs-core component and get full params
        back'''
        try:
            out, err = Simulation.call_simfs(
                    self.call, 
                    *self.opts, 
                    'list', 
                    **self.params
                    )
            self.err = err
            self._params = out
        except Exception as e:
            print('Error calling SiMFS.', self.call, e)
            return

    def __repr__(self):
        return f'{self.name}'

    ########################################################################### 
    @property
    def inputs(self):
        inputs = set()
        for p in self.__class__.input_paths:
            val = Component.get_dict_path(self._params, p.name.split('/'))
            inputs.update({IO(v, p.dtype) for v in val})
        return inputs

    ########################################################################### 
    def remap_inputs(self, mapping):
        for p in self.__class__.input_paths:
            Component.set_dict_path(self._params, p.name.split('/'), mapping)

    ########################################################################### 
    @property
    def outputs(self):
        outputs = set()
        for p in self.__class__.output_paths:
            val = Component.get_dict_path(self._params, p.name.split('/'))
            outputs.update({IO(v, p.dtype) for v in val})
        return outputs

    ########################################################################### 
    def remap_outputs(self, mapping):
        for p in self.__class__.output_paths:
            Component.set_dict_path(self._params, p.name.split('/'), mapping)

   ########################################################################### 
    @staticmethod
    def get_dict_path(d, keys):
        if type(d) is not dict:
            return {}
        if len(keys) == 1:
            val = d.get(keys[0])
            if type(val) == list:
                return set(val)
            if val:
                return {val}
            return {}
        if keys[0] == '*':
            vals = set()
            for key in d.keys():
                vals.update(Component.get_dict_path(d.get(key), keys[1:]))
            return vals
        return Component.get_dict_path(d.get(keys[0]), keys[1:])


    ########################################################################### 
    @staticmethod
    def set_dict_path(d, keys, mapping):
        if type(d) is not dict:
            return
        if len(keys) == 1:
            val = d.get(keys[0])
            if type(val) == list:
                d[keys[0]] = list(map(lambda x: mapping.get(x, x), d[keys[0]]))
                return
            if val:
                d[keys[0]] = mapping.get(val, val)
        if keys[0] == '*':
            for key in d.keys():
                Component.set_dict_path(d.get(key), keys[1:], mapping)
        Component.set_dict_path(d.get(keys[0]), keys[1:], mapping)


###############################################################################
# Component interfaces
###############################################################################

###############################################################################
class Diffusion(Component):    
    cmd = 'mol/simfs_dif'
    output_paths = [
        IO('coordinate_output', coordinate_t),
        IO('collision_output', timetag_t)
    ]

###############################################################################

class Conformation(Component):
    cmd = 'mol/simfs_cnf'
    output_paths = [
        IO('output', timed_value_t),
    ]

###############################################################################

class Shift(Component):  
    cmd = 'mol/simfs_sft'
    input_paths = [
        IO('input', coordinate_t),
    ]
    output_paths = [
        IO('output', coordinate_t),
    ]

###############################################################################

class Fluorophore(Component):
    cmd = 'ph2/simfs_ph2'
    input_paths = [
        IO('jablonsky/*/rate/input', timed_value_t),
        IO('jablonsky/*/trigger/input', timetag_t)
    ]
    output_paths = [
        IO('jablonsky/*/output', timetag_t),
        IO('jablonsky/*/trigger/output', timetag_t)
    ]

###############################################################################
class CoordinateBuffer(Component):
    cmd = 'utl/simfs_buf'
    input_paths = [
        IO('input', coordinate_t),
    ]
    output_paths = [
        IO('outputs', coordinate_t),
    ]

###############################################################################
class TimedValueBuffer(Component):
    cmd = 'utl/simfs_buf'
    input_paths = [
        IO('input', timed_value_t),
    ]
    output_paths = [
        IO('outputs', timed_value_t),
    ]

###############################################################################
class TimetagBuffer(Component):
    cmd = 'utl/simfs_buf'
    input_paths = [
        IO('input', timetag_t),
    ]
    output_paths = [
        IO('outputs', timetag_t),
    ]

###############################################################################
class Mixer(Component):
    cmd = 'utl/simfs_mix'
    input_paths=[
        IO('inputs', timetag_t),
    ]
    output_paths=[
        IO('output', timetag_t),
    ]

###############################################################################
class Splitter(Component):
    cmd = 'utl/simfs_spl'
    input_paths=[
        IO('photon_input', timetag_t),
        IO('efficiency_input', timed_value_t)
    ]
    output_paths=[
        IO('accepted_output', timetag_t),
        IO('rejected_output', timetag_t)
    ]

###############################################################################
class Excitation(Component):
    cmd = 'fcs/simfs_exi'
    input_paths=[
        IO('input', coordinate_t),
    ]
    output_paths=[
        IO('output', timed_value_t),
    ]

###############################################################################
class Detection(Component):
    cmd = 'fcs/simfs_det'
    input_paths=[
        IO('input', coordinate_t),
    ]
    output_paths=[
        IO('output', timed_value_t),
    ]

###############################################################################
class Precalculate(Component):
    cmd = 'fcs/simfs_pre'
    input_paths=[ ]
    output_paths=[ ]


###############################################################################
class Pulse(Component):
    cmd = 'fcs/simfs_pls'
    input_paths=[
        IO('input', timed_value_t),
    ]
    output_paths=[
        IO('output', timed_value_t),
    ]

###############################################################################
class Imager(Component):
    cmd = 'utl/simfs_img'
    input_paths=[
        IO('coordinate_inputs', coordinate_t),
        IO('time_inputs', timetag_t)
    ]
            
