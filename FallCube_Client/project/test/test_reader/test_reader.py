import os
import pytest

from reader.reader import Reader

@pytest.fixture
def file_path():
    """
    Fixture to set file path and categories to read
    """

    return {
        'path': os.path.join(os.path.dirname(__file__), 'test_bookings.csv'),
        'cat': ['room','start','end']
    }

def test_successful_open_read_in_data(file_path):
    """
    Checks that reading a file successfully returns some data 
    """

    assert Reader.read_in_data(file_path['path'], file_path['cat']) != {}

def test_successful_read_read_in_data(file_path):
    """
    Checks data read is correct
    """

    file_data = Reader.read_in_data(file_path['path'], file_path['cat'])
    expected_data = {
        'start': ['01/01/1970:00:00', '01/01/1970:00:01'], 
        'room': ['g1', 'f1'], 
        'end': ['01/01/1970:01:00', '01/01/1970:00:02'], 
    }

    for col, data in expected_data.items():
        assert col in file_data
        for idx, val in enumerate(data):
            assert file_data[col][idx] == val

def test_invalid_file_read_in_data(file_path):
    """
    Checks invalid file path error is handled
    """

    with pytest.raises(FileNotFoundError):
        Reader.read_in_data('RANDOM_INCORRECT_PATH', file_path['cat']) != {}

def test_invalid_catergory_read_in_data(file_path):
    """
    Checks expecting a different column header error is handled 
    """

    assert Reader.read_in_data(file_path['path'], ['RANDOM_INCORRECT_CAT']) == {}
