import os

from . pipe import BasePipe

class UnixPipe(BasePipe):
    '''Pipe handler implementation that uses UNIX named pipes'''

    def __init__(self, path: str) -> None:
        self._path = path

    def __str__(self) -> str:
        return str(self.path)

    def __enter__(self):
        os.mkfifo(self._path)
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        if os.path.exists(self._path):
            os.remove(self._path)
        
    @property
    def path(self) -> str:
        return self._path
