import pytest
#import collections
import os
from pytest_mock import mocker
#from pyfakefs.fake_filesystem_unittest import Patcher

from file_tracking.monitor import Monitor

from threading import Thread

def monitor_setup(mock_func, fake_input_dir):
    """
    Set up monitor and mock call back
    """

    monitor = Monitor(fake_input_dir, mock_func)
    monitor.run()

def test_run_create_success(tmpdir, mocker):
    """
    Check that ScanOnce can correctly read files/ directories on file system
    """
    path_to_me = ''#os.path.dirname(__file__)
    fake_input_dir = 'FAKE_INPUT'
    print(fake_input_dir)
    #fs.create_dir(fake_input_dir)
    tmpdir.mkdir(fake_input_dir)
    
    mock_func = mocker.Mock()
    t = Thread(target=monitor_setup, args=(mocker, fake_input_dir))
    t.start()
    #fs.create_dir(fake_input_dir + '/a')
    #assert os.path.exists(fake_input_dir + os.sep + 'a')
    tmpdir.mkdir(fake_input_dir + os.sep + 'a')
    #assert os.path.exists(fake_input_dir + os.sep + 'a')
    #monitor_setup.fs.create_file('PATH TO DIR/a/f1.txt')
    mock_func.assert_called_with('created|dir', '', 'a')
    #monitor_setup.call_back.assert_any_call('created|file', '\\a', 'f1.txt')

    #t.join()
