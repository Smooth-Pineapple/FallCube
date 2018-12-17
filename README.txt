===========================================
McLaren Racing
Code at Home Excercise - Room Booking
===========================================

** RoomBooking **

This Python program takes two CSV files as input. The first, representing valid rooms to book, and second, listing booking attempts. Then either reserves the room or detects errors/ booking conflicts, and prints the unsuccessful booking information to stdout.

===========================================

** Usage **

* Build * 
From the project root ('RoomBooking/') run the following in command prompt:

    pyinstaller --onefile project\main.py --name RoomBooking

This uses the 'pyinstaller' tool to create the 'RoomBooking' executable, placing it in the 'RoomBooking/dist' directory. This executable can be run from command prompt like so:

    RoomBooking.exe ..\project\res\rooms.csv  ..\project\res\bookings.csv

Here the executable is being run from the 'dist' directory. It's usage is as follows:

    RoomBooking.exe [relative_room_data_file_path] [relative_booking_data_file_path]

* Run *
From the project root ('RoomBooking/') run the following in command prompt:

    py project\main.py res\rooms.csv res\bookings.csv

Here 'project\main.py' signals the main Python file to run, 'res\rooms.csv' is the valid room input file, 'res\bookings.csv' is the booking request input file

* Test *
Automated tests have been implemented using the 'pytest' module, from the project root ('RoomBooking/') run the following in command prompt to use:

    pytest -v

The tests in 'test_reader.py' use the 'test_bookings.csv' file as input.

===========================================

** Input **

* room_data_file *
A comma-separated input file representing the rooms available to be booked. It has the following format:
    room
    [room_id]
    [room_id]
    [room_id]
    ....

* booking_data_file *
A comma-separated input file representing requests to book rooms (rooms must be defined in 'room_data_file') at a certain time. It has the following format:
    room,start,end
    [room_id],[start_datetime],[end_datetime]
    [room_id],[start_datetime],[end_datetime]
    [room_id],[start_datetime],[end_datetime]
    ....

The 'start_datetime' and 'end_datetime' have the following format:
    dd/mm/yy:hh:mm

Example:
    25/12/2018:14:30

Note:
The 'end_datetime' date must be the same as the 'start_datetime' date.

* Output *
The program will output errors relating to invalid bookings, and information detailing conflicted bookings.

A more verbose output of the entire booking information (detailing the usage of every room, for every 'start_datetime' date, specified in the 'booking_data_file') can be shown with the '-v' argument:

    RoomBooking.exe ..\project\res\rooms.csv  ..\project\res\bookings.csv -v

===========================================

** Requirements **

- Built with latest Python version (python-3.7.1).
- Ensure the Python install directory is added to your PATH environment variable.
- Ensure 'pip' can install modules, and that they are runnable from the command line.
- Install 'pandas', 'pyinstaller' and 'pytest' using 'pip'
- To use VSCode features (debugging/running/building/tests) ensure VSCode is installed (Version: 1.28.2), '${workspaceRoot}' is set to 'RoomBooking' root and that the 'python.pythonPath' setting in the '.vscode/settings.json' file is set to the your Python executable path. 
- Remove 'GMAIL_FIX' before running pre-built executable.

===========================================

** RoomBooking directory structure **

RoomBooking/
    .vscode/
        launch.json                         (Allows debugging with VSCode)
        settings.json                       (Set 'python.pythonPath' to your Python executable path to use VSCode features)
        tasks.json                          (Allows running/building/testing of program with VSCode 'Run Task...' option, there is also a task to install dependencies)
    dist/
        RoomBooking.exe.GMAIL_FIX           (Pre-built executable of 'RoomBooking' program, remove 'GMAIL_FIX' before running)
    project/
        booking/                            (Contains booking related classes)
            booking_manager.py              (Handles booking validity)
            room.py                         (Class to represent room availability)
        datetime_formater/                  
            datetime_formater.py            (Static helper for date and time conversions)
        reader/                        
            reader.py                       (Static helper for CSV parsing)
        res/                                (Contains sample CSV files)
            bookings.csv                    (Sample booking requests CSV)
            rooms.csv                       (Sample valid room CSV)
        test/                               (Contains automated tests for 'RoomBooking')
            test_booking/
                test_booking_manager.py
            test_datetime_formater/
                test_datetime_formater.py
            test_reader/
                test_booking.csv
                test_reader.py
        main.py                             (Program entry point)
    README.txt

===========================================