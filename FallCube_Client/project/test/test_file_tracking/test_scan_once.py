import pytest
import os

from pytest_mock import mocker
from pyfakefs.fake_filesystem_unittest import Patcher

from file_tracking.scan_once import ScanOnce

@pytest.fixture
def fake_filesystem(fs):
    """
    Set up fake filesystem
    """

    fs.create_dir('PATH TO DIR' + os.sep + 'a' + os.sep +  'b')
    fs.create_file('PATH TO DIR' + os.sep + 'f1.txt')
    fs.create_file('PATH TO DIR' + os.sep + 'a' + os.sep + 'b' + os.sep + 'f2.txt')


    return fs

def test_run_success(fake_filesystem, mocker):
    """
    Check that ScanOnce can correctly read files/ directories on file system
    """

    mock_func = mocker.Mock()
    scan_once = ScanOnce('PATH TO DIR', mock_func)
    scan_once.run()

    mock_func.assert_any_call('created|file', '', 'f1.txt')
    mock_func.assert_any_call('created|dir', os.sep + 'a', 'b')
    mock_func.assert_any_call('created|dir', '', 'a')
    mock_func.assert_any_call('created|file', os.sep + 'a' + os.sep + 'b', 'f2.txt')