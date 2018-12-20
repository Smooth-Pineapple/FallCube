import pytest
import os

#from pytest_mock import mocker
from pyfakefs.fake_filesystem_unittest import Patcher

from sync.file_io_sync import FileIOSync

@pytest.fixture
def fake_filesystem(fs):
    """
    Set up fake filesystem
    """

    fs.create_dir('a')
    fs.create_file('f1.txt')
    fs.create_file('a' + os.sep + 'f2.txt')
    fs.create_dir('c')
    fs.create_dir('c' + os.sep + 'f3.txt')
    fs.create_dir('c' + os.sep + 'd')

    return fs

@pytest.fixture
def file_io_sync(fake_filesystem):
    """
    Simply create a FileIOSync object
    """

    sync = FileIOSync('')

    return sync

def test_set_sync_action(file_io_sync):
    """
    Check that FileIOSync can properly understand events
    """

    assert file_io_sync.set_sync_action('created', 'file', 'f1.txt') == 'end' # As already exists
    assert file_io_sync.set_sync_action('deleted', 'dir', 'b') == 'end' # As can't modify something that doesn't exist
    assert file_io_sync.set_sync_action('created', 'file', 'f2.txt') == 'read' # As it's a new file
    assert file_io_sync.set_sync_action('created', 'dir', 'b') == 'create' # As it's a new directory
    assert file_io_sync.set_sync_action('modified', 'file', 'f1.txt') == 'read' # As a modification to a file's contents
    assert file_io_sync.set_sync_action('moved', 'dir', 'a') == 'rename' # As changed the name of a file/ directory
    assert file_io_sync.set_sync_action('deleted', 'file', 'a' + os.sep + 'f2.txt') == 'remove' # As removed a file
    assert file_io_sync.set_sync_action('FAKE', 'dir', 'a') == 'err' # As event isn't understood

def test_file_sync(file_io_sync):
    """
    Test file creation, writing and closure flow
    """

    file_io_sync.set_file_sync('f2.txt')
    file_io_sync.sync_file_data(b'hello')
    file_io_sync.end_file_sync()

    assert os.path.exists('f2.txt')

    f = open('f2.txt', "r")
    assert f.read() == 'hello'
    f.close()

def test_sync_dir(file_io_sync):
    """
    Test creation of directory
    """

    file_io_sync.sync_dir('b')
    assert os.path.exists('b')


def test_sync_delete(file_io_sync):
    """
    Test deletion of file/ directory
    """

    file_io_sync.sync_delete('f1.txt')
    assert not os.path.exists('f1.txt')

    file_io_sync.sync_delete('a')
    assert not os.path.exists('a')
    assert not os.path.exists('a' + os.sep + 'f2.txt')

def test_sync_rename(file_io_sync):
    """
    Test renaming of file/ directory
    """

    file_io_sync.sync_rename('c' + os.sep + 'f4.txt', 'c' + os.sep + 'f3.txt')

    assert os.path.exists('c' + os.sep + 'f4.txt')
    assert not os.path.exists('c' + os.sep + 'f3.txt')

    file_io_sync.sync_rename('c' + os.sep + 'e', 'c' + os.sep + 'd')

    assert os.path.exists('c' + os.sep + 'e')
    assert not os.path.exists('c' + os.sep + 'd')

   