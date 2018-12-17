import pytest

from booking.booking_manager import BookingManager

@pytest.fixture
def booking_manager():
    """
    Fixture to set valid rooms path, create BookingManager object and checks that booking a room for the first time is successful
    """

    valid_rooms = ['g1','f1']

    bm = BookingManager(valid_rooms)  
    severe_failure, errMsg = bm.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':0, 'end_time':1})
    assert severe_failure == False and errMsg == ""

    return bm

def test_successful_add_booking(booking_manager):
    """
    Checks that the booking to a room between bookings is succesful
    """

    booking_manager.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':2, 'end_time':3})
    
    severe_failure, errMsg = booking_manager.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':1, 'end_time':2})
    assert severe_failure == False and errMsg == ""

def test_overlapping_add_booking(booking_manager):
    """
    Checks that double booking of a room is handled
    """

    severe_failure, errMsg = booking_manager.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':0, 'end_time':2})
    assert severe_failure == False and errMsg != ""

def test_invalid_add_booking(booking_manager):
    """
    Checks that the invalid booking of a room is handled
    """

    # Check can't book over multiple days
    severe_failure, errMsg = booking_manager.add_booking('g1', {'start_day':1, 'end_day':200}, {'start_time':0, 'end_time':1})
    assert severe_failure == False and errMsg != ""

    # Check can't book a non-valid room
    severe_failure, errMsg = booking_manager.add_booking('FAKE_ROOM', {'start_day':1, 'end_day':1}, {'start_time':0, 'end_time':1})
    assert severe_failure == False and errMsg != ""

    # Check can't book a room with invalid keys
    severe_failure, errMsg = booking_manager.add_booking('g1', {'FAKE_KEY':1, 'end_day':1}, {'start_time':5, 'end_time':6})
    assert severe_failure == True and errMsg != ""

def test_successful_get_bookings(booking_manager):
    """
    Checks the gathering of room booking data
    """

    # Check that some get returns a success
    reservation_data, errMsg = booking_manager.get_bookings('g1', 1)
    assert reservation_data != [] and errMsg == ""

    expected_data = [
        {
            'end_time': 1, 
            'start_time': 0
        }
    ]

    # Check that booking information is correct
    assert len(expected_data) == len(reservation_data)
    
    for idx, time in enumerate(expected_data):
        assert reservation_data[idx]['start_time'] == time['start_time']
        assert reservation_data[idx]['end_time'] == time['end_time']

def test_invalid_get_bookings(booking_manager):
    """
    Checks that the gathering of booking data handles situations where no data is present
    """

    # Unbooked but valid rooms 
    reservation_data, errMsg = booking_manager.get_bookings('f1', 1)
    assert reservation_data == [] and errMsg != ""

    # Valid room but non-booked day
    reservation_data, errMsg = booking_manager.get_bookings('g1', 200)
    assert reservation_data == None and errMsg != ""

    # Invalid room
    reservation_data, errMsg = booking_manager.get_bookings('FAKE_ROOM', 1)
    assert reservation_data == [] and errMsg != ""