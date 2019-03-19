#! /usr/bin/env python

'''Tests for pysimfs pipe utility.'''

#-----------------------------------------------------------------------------#

# stdlib
import os
import threading

# 3rd party
from hypothesis import given, example
from hypothesis.strategies import binary
import numpy as np
import pytest

# package
from pysimfs.pipe import Pipe

#-----------------------------------------------------------------------------#

@pytest.fixture(scope='module')
def tmp_dir(tmpdir_factory) -> str:
    return tmpdir_factory.mktemp('pipes')

@pytest.fixture
def pipe_instance(tmp_dir) -> Pipe:
    '''Creates a pipe in a temporary directory'''
    return Pipe(os.path.join(tmp_dir, 'pipe1'))

#-----------------------------------------------------------------------------#

@pytest.mark.parametrize('repeat', range(3))
def test_create(repeat, pipe_instance):
    '''Create a sigle pipe and check the path's suffix'''
    with pipe_instance as p:
        assert p.path.endswith('pipe1')

def test_get_path_from_string(pipe_instance):
    '''Retrieve the qualified path from the string representation'''
    assert str(pipe_instance).endswith('pipe1')

def test_file_exists_error(pipe_instance):
    '''If a file already exists, an error is raised'''
    with pipe_instance as p1:                   # open pipe 1
        with pytest.raises(FileExistsError):    # expect an error
            with Pipe(p1.path):                 # open pipe 2
                pass

#-----------------------------------------------------------------------------#

def writer(path: str, data: bytes) -> threading.Thread:
    '''Utility: starts a thread to write data to the file spcified by path.'''

    def _writer():
        with open(path, 'wb') as f:
            f.write(data)

    thread = threading.Thread(target=_writer)
    thread.start()
    return thread


@given(binary())
@example(b'')
def test_read_write(pipe_instance, data):
    '''Write and read arbitrary bianry data to and from a named pipe'''

    with pipe_instance:

        writer_thread = writer(pipe_instance.path, data)
        with open(pipe_instance.path, 'rb') as f:
            result = f.read()

        assert result == data
        writer_thread.join()

#-----------------------------------------------------------------------------#


