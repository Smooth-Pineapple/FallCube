===========================================
Pexip
FallCube
===========================================

** FallCube **

FallCube synchronises a source and destination folder over IP. 
This Python workspace consists of 2 projects. The 'FallCube_Client' which monitors a directory for files/ directories, and the 'FallCube_Server' which takes messages from the client(over IP) and recreates the monitored directory.

===========================================

** Usage **

* Build * 
From the workspace root ('FallCube/') run the following in command prompt:

    pyinstaller --onefile FallCube_Client/project/main.py --name FallCube_Client
    pyinstaller --onefile FallCube_Server/project/main.py --name FallCube_Server

This uses the 'pyinstaller' tool to create the 'FallCube_Client'/'FallCube_Server' executable, placing it in the 'FallCube/dist' directory. These executables can be run from command prompt like so:

    FallCube_Client.exe ../FallCube_Client/project/test/fake_input_dir 127.0.0.1 12345
    FallCube_Server.exe ../FallCube_Server/project/test/fake_output_dir 127.0.0.1 12345

Here the executables are being run from the 'dist' directory. Their usage is as follows:

    [PROGRAM NAME] [INPUT DIRECTORY FOR CLIENT OR EMPTY OUTPUT DIRECTORY FOR SERVER] [IP ADDRESS] [PORT]

* Run *
From the project root ('FallCube/') run the following in command prompt:

    py FallCube_Client/project/main.py FallCube_Client/project/test/fake_input_dir 127.0.0.1 12345
    py FallCube_Server/project/main.py FallCube_Server/project/test/fake_output_dir 127.0.0.1 12345

Here 'main.py' signals the main Python file to run, 'fake_input_dir'/'fake_output_dir' are the valid synchronise directory inputs, '127.0.0.1' is the host address and '12345' is the port.

* Test *
Automated tests have been implemented using the 'pytest' module, from the project root ('FallCube/') run the following in command prompt to use:

    pytest FallCube_Client/ -v
        OR
    pytest FallCube_Server/ -v    

===========================================

** Requirements **

- Built with latest Python version (python-3.7.1).
- Ensure the Python install directory is added to your PATH environment variable.
- Ensure 'pip' can install modules, and that they are runnable from the command line.
- Install 'watchdog', 'pyinstaller', 'pytest', 'pyfakefs' and 'pytest-mock' using 'pip'
- To use VSCode features (debugging/running/building/tests) ensure VSCode is installed (Version: 1.28.2), '${workspaceRoot}' is set to the 'FallCube' root and that the 'python.pythonPath' setting in the '.vscode/settings.json' file is set to the your Python executable path. 

===========================================

** FallCube directory structure **

FallCube/
    .vscode/
        launch.json                             (Allows debugging with VSCode)
        tasks.json                              (Allows running/building/testing of FallCube with VSCode 'Run Task...' option, there is also a task to install dependencies)
    FallCube_Client/                            (Project to monitor a directory)
        project/
            file_tracking/                      (Contains filesystem monitoring classes)
                scan_once.py                    (Performs one-time scan of a directory)
                file_tracking.py                (Abstract base class for filesystem tracking)
                monitor.py                      (Performs continuous monitoring of filesystem)
                monitor_handle.py               (Handler for filesystem events)
            file_transfer/                      (Contains server synchronisation classes)
                data_sender.py                  (Class for direct socket communication)
                file_transfer.py                (Sends filesystem information and file data to the server)
            test/                               (Contains automated tests for 'FallCube_Client')
                fake_input_dir/                 (Can optionally use this as a directory for the client to monitor)
                test_file_tracking/
                    test_file_tracking.py
                    test_monitor_handle.py
                    test_scan_once.py
                test_file_transfer/
                    test_data_sender.py
                    test_file_transfer.py
            main.py                             (FallCube_Client entry point)
    FallCube_Server/                            (Project to synchronise with client over IP)
        project/
            sync/                               (Contains synchronisation method classes)
                sync.py                         (Abstract base class for synchronisation)
                file_io_sync.py                 (Performs file based synchronisation(e.g. deleting a directory, creating a new file on the filesystem))
            file_transfer/                      (Contains server synchronisation classes)
                data_receiver.py                (Class for direct socket communication)
                file_transfer.py                (Listens for client messages and invokes the appropiate synchronisation method(e.g. make a new file, rename a directory...))
            test/                               (Contains automated tests for 'FallCube_Server')
                test_sync/
                    test_file_io_sync.py
                test_file_transfer/
                    test_data_receiver.py
                    test_file_transfer.py
            main.py                             (FallCube_Server entry point)        
    README.txt

===========================================