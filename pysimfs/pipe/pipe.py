class BasePipe():

    '''Abstract pipe handler that manages the lifetime of a named pipe'''

    def __init__(self, name):
        '''Creates a named pipe handler'''
        raise NotImplementedError

    def __enter__(self):
        '''Creates the filesystem pipe object'''
        raise NotImplementedError

    def __exit__(self, ex_type, ex_value, traceback):
        '''Deletes the filesystem pipe object'''
        raise NotImplementedError

    @property
    def path(self):
        '''The full path to the named pipe'''
        raise NotImplementedError
