import pytest
import datetime

from datetime_formater.datetime_formater import DateTimeFormater

def test_successful_to_date_and_time_lists():
    """
    Checks conversion from datetime string to date and time list is correct
    """

    expected_data = ['01/01/1970:00:00', '01/01/1970:00:01']
    expected_dates = [datetime.date(1970, 1, 1), datetime.date(1970, 1, 1)]
    expected_times = [datetime.time(0, 0), datetime.time(0, 1)]


    date_lis, time_lis = DateTimeFormater.to_date_and_time_lists(expected_data)
    assert date_lis is not None or time_lis is not None # Firstly ensure some data is returned

    # Now check data is correct    
    assert len(expected_dates) == len(date_lis) and len(expected_times) == len(time_lis)
    
    for idx, date in enumerate(expected_dates):
        assert date_lis[idx] == date
    for idx, time in enumerate(expected_times):
        assert time_lis[idx] == time

def test_unsuccessful_to_date_and_time_lists():
    """
    Checks invalid datetime string error is handled
    """

    expected_data = ['31/02/1970:00:00', '01/01/1970:00:01']

    date_lis, time_lis = DateTimeFormater.to_date_and_time_lists(expected_data)
    assert date_lis is None and time_lis is None

def test_successful_days_from_epoch_date():
    """
    Checks conversion from date to days is correct
    """
        
    assert DateTimeFormater.days_from_epoch_date(datetime.date(1970, 1, 5)) == 4
        
def test_unsuccessful_days_from_epoch_date():
    with pytest.raises(ValueError):
        """
        Checks conversion from invalid date to days is handled
        """    

        DateTimeFormater.days_from_epoch_date(datetime.date(1970, 100, 1))

def test_epoch_date_from_days():
    """
    Checks conversion from days to date is correct
    """

    assert DateTimeFormater.epoch_date_from_days(4).date() == datetime.date(1970, 1, 5)

def test_time_to_minutes():
    """
    Checks conversion from time to minutes is correct
    """

    assert DateTimeFormater.time_to_minutes(datetime.time(18, 10)) == 1090

def test_minutes_to_time():
    """
    Checks conversion from minutes to time is correct
    """

    assert DateTimeFormater.minutes_to_time(1090).strftime("%H:%M") == datetime.time(18, 10).strftime("%H:%M")
    
        