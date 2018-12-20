import pytest
from pytest_mock import mocker

import pytest
from pytest_mock import mocker

from file_tracking.file_tracking import FileTracking

class FileTrackingImpl(FileTracking):
    """
    Simple implementation of abstract FileTracking class
    """

    def run(self):
        pass

    def callback_with_relevant_path_stripper(self, action, path, file, old_path = None):
        """
        Wrapper to call internal method
        """

        super()._callback_with_relevant_path_stripper(action, path, file, old_path)


def test_callback_with_relevant_path_stripper_success(mocker):
    """
    Check base path is correctly removed from found file/ directory
    """

    mock_func = mocker.Mock()
    file_tracking = FileTrackingImpl('PATH TO DIR', mock_func)

    file_tracking.callback_with_relevant_path_stripper('PASS THROUGH ACTION', 'PATH TO DIR ONLY_THIS_SHOULD_REMAIN', 'PASS THROUGH FILE', 'WE_SHOULD_ALL_REMAIN_PATH_TO_DIR')
    mock_func.assert_called_with('PASS THROUGH ACTION', ' ONLY_THIS_SHOULD_REMAIN', 'PASS THROUGH FILE', 'WE_SHOULD_ALL_REMAIN_PATH_TO_DIR')

    file_tracking.callback_with_relevant_path_stripper('PASS THROUGH ACTION', 'PATH TO 123 DIR', 'PASS THROUGH FILE', 'PATH TO DIR')
    mock_func.assert_called_with('PASS THROUGH ACTION', 'PATH TO 123 DIR', 'PASS THROUGH FILE', '')
    
    file_tracking.callback_with_relevant_path_stripper('1', 'PATH TO', '2', 'PATH TO DIR/SOME FILE')
    mock_func.assert_called_with('1', 'PATH TO', '2', '/SOME FILE')
