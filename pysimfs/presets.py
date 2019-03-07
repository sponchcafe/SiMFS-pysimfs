from IPython.core.magic import Magics, magics_class, line_magic
import json
from pysimfs import Simulation, Component
from . import basepath
import os

###############################################################################
@magics_class
class SimfsDefaultMagics(Magics):

    ###########################################################################
    shortcuts = {
            'dif': os.path.join('mol', 'simfs_dif'),
            'cnf': os.path.join('mol', 'simfs_cnf'),
            'sft': os.path.join('mol', 'simfs_sft'),
            'exi': os.path.join('fcs', 'simfs_exi'),
            'det': os.path.join('fcs', 'simfs_det'),
            'pls': os.path.join('fcs', 'simfs_pls'),
            'pre': os.path.join('fcs', 'simfs_pre'),
            'ph2': os.path.join('ph2', 'simfs_ph2'),
            'spl': os.path.join('utl', 'simfs_spl'),
            'mix': os.path.join('utl', 'simfs_mix'),
            'buf': os.path.join('utl', 'simfs_buf'),
            'img': os.path.join('utl', 'simfs_img')
            }

    ###########################################################################
    @line_magic
    def simfs_default(self, line):

        args = line.split()
        comp = args[0]
        call = os.path.join(basepath, SimfsDefaultMagics.shortcuts[comp])

        '''
        params = dict(
            (k.strip(), literal_eval(v.strip())) for (k, v) in 
            map(lambda s: s.split('='), args[1:].split(','))
        )
        '''

        params = Simulation.call_simfs(call, 'list')[0]
        cell_content = f'{line.split("/")[-1]}_params = '
        cell_content+= json.dumps(params, indent=4).replace('"', "'")

        self.shell.set_next_input(
                f'# %simfs_default {line}\n{cell_content}', 
                replace=True
                )
