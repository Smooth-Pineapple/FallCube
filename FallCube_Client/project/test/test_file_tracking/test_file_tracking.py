import pytest


@pytest.fixture
def file_tracking():
    """
    """

    from file_tracking.file_tracking import FileTracking

    class FileTrackingImpl(FileTracking):
        def run(self):
            pass

        def callback_with_relevant_path_stripper(self, action, path, file, old_path = None):
            super()._callback_with_relevant_path_stripper(self, action, path, file, old_path = None)

    fti = FileTrackingImpl('PATH TO DIR', )

    return fti

def call_back(self, event, dir, file, old_file = None):
   


def test_callback_with_relevant_path_stripper(file_tracking):
    """
    """

    file_tracking.callback_with_relevant_path_stripper('PASS THROUGH ACTION', 'PATH TO DIR ONLY_THIS_SHOULD_REMAIN', 'PASS THROUGH FILE', 'WE_SHOULD_ALL_REMAIN_PATH_TO_DIR')

