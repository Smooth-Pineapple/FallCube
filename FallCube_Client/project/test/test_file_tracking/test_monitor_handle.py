import pytest
import os
import collections

from pytest_mock import mocker
from pyfakefs.fake_filesystem_unittest import Patcher

from file_tracking.monitor_handle import MonitorHandle

MonitorSetup = collections.namedtuple('MonitorSetup', 'fs monitor_handle call_back')

class MonitorHandleWrapper(MonitorHandle):
    """
    Simple wrapper class to allow access to internal event handler 
    """

    def handle_event(self, isDir, eType, path_file, path_old_file = None):
       super()._handle_event(isDir, eType, path_file, path_old_file)


@pytest.fixture
def monitor_setup(fs, mocker):
    """
    Set up fake filesystem, return monitor object to check
    """

    fs.create_file('f1.txt')
    fs.create_dir('a')
    fs.create_dir('b')
    fs.create_file('b' + os.sep + 'f2.txt')

    mock_func = mocker.Mock()
    monitor_handle = MonitorHandleWrapper(mock_func)

    ms = MonitorSetup(fs, monitor_handle, mock_func)
    return ms
	
	
def test_on_created_success(monitor_setup):
    """
    Check that creation events are handled
    """

    monitor_setup.monitor_handle.handle_event(False, 'created', 'f1.txt')
    monitor_setup.monitor_handle.handle_event(True, 'created', 'a')
    monitor_setup.monitor_handle.handle_event(True, 'created', 'b')

    monitor_setup.call_back.assert_any_call('created|file', '', 'f1.txt', None)
    monitor_setup.call_back.assert_any_call('created|dir', '', 'a', None)
    monitor_setup.call_back.assert_any_call('created|dir', '', 'b', None)


def test_on_modified_success(monitor_setup):
    """
    Check that modification events are handled
    """

    monitor_setup.monitor_handle.handle_event(False, 'modified', 'f1.txt')

    monitor_setup.call_back.assert_any_call('modified|file', '', 'f1.txt', None)
	
	
def test_on_moved_success(monitor_setup):
    """
    Check that renaming events are handled
    """

    monitor_setup.fs.rename('b', 'c') 

    monitor_setup.monitor_handle.handle_event(False, 'moved', 'c' + os.sep + 'f2.txt', 'b' + os.sep + 'f2.txt')
    monitor_setup.monitor_handle.handle_event(True, 'moved', 'c', 'b')

    monitor_setup.call_back.assert_any_call('moved|dir', '', 'c', 'b')
    monitor_setup.call_back.assert_any_call('moved|file', 'c', 'f2.txt', 'b' + os.sep + 'f2.txt')
	
def test_on_deleted_success(monitor_setup):
    """
    Check that deletion events are handled
    """

    monitor_setup.monitor_handle.handle_event(True, 'deleted', 'b')

    monitor_setup.call_back.assert_any_call('deleted', '', 'b', None)
	
	