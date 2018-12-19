import pytest

import os

@pytest.fixture
def scan_once():
    """
    Fixture to set valid rooms path, create BookingManager object and checks that booking a room for the first time is successful
    """

    from file_tracking.scan_once import ScanOnce

    fake_input_dir_path = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'fake_input_dir'
    scan_once = ScanOnce(fake_input_dir_path, call_back)

    return scan_once
def call_back(self, event, dir, file, old_file = None):
    """
    Attempts to transfer files/ directories to server 
    Input: 
        event: type of file system event (created, modified, deleted, moved), and whether it applies to a file/ directory
        dir: path to directory containing affected file/ directory  
        file: file/ directory that is relevant to event
        old_file: (optional) if renaming(moved) this will contain path to the old file/ directory(inc path)
    """

    # Object to handle server communication
    data_sender = DataSender(self.__host, self.__port)

    try:
        # Full path to affected file/ directory
        to_file = dir + os.sep + file
        if old_file:
            # Append previous path to affected file/ directory(renaming)
            to_file += '|' + old_file

        # Message to send to server, format:
            # [EVENT]|[FILE/DIRECTORY]|[PATH FROM MONITORED DIRECTORY TO FILE/ DIRECTORY]...also can have...|[PATH FROM MONITORED DIRECTORY TO OLD FILE/ DIRECTORY]
        client_msg = event + "|" + to_file
        print("Message to send to server:", client_msg)
        
        # Send message and wait for response
        server_response = data_sender.notify(client_msg)
        # If server is expecting to read file data, open local file and send data to server
        if server_response == 'read':
            file_to_parse = open(self.__base_dir + to_file, 'rb') 
            data_sender.send_data(file_to_parse)
            file_to_parse.close()

    except FileNotFoundError as e:
        print("File not found:", e)   
    except socket.timeout as e:
        print("Socket timeout:", e) 
    except socket.error as e:
        print("Error in socket connection:", e)    
    except socket.gaierror as e:
        print("Error with address:", e)         
    except:
        print("Unexpected error:", sys.exc_info()[0])         
    finally:  
        data_sender.close() # Explicitly close even though destructor will do it anyway           


def test_successful_add_booking(booking_manager):
    """
    Checks that the booking to a room between bookings is succesful
    """

    booking_manager.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':2, 'end_time':3})
    
    severe_failure, errMsg = booking_manager.add_booking('g1', {'start_day':1, 'end_day':1}, {'start_time':1, 'end_time':2})
    assert severe_failure == False and errMsg == ""
