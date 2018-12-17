import os
import sys

from file_tracking.file_tracking import FileTracking
from file_tracking.monitor import Monitor
from file_tracking.scan_once import ScanOnce

from file_transfer.file_transfer import FileTransfer

# Main entry point
def main():
    # Ensure valid usage
    if len(sys.argv) < 4 or sys.argv[1] == '-h' or not sys.argv[3].isnumeric():
        print("Usage:", os.path.basename(__file__), "monitor_dir server_path server_port\n")
      
        return 

    file_transfer = FileTransfer(sys.argv[1], sys.argv[2], sys.argv[3])
    file_tracker = [ScanOnce(sys.argv[1], file_transfer.transfer), Monitor(sys.argv[1],  file_transfer.transfer)]
    for tracker in file_tracker:
        tracker.run()
        
    # parse dir
    # send each file to serv
    # monitor dir
        # send each new to serv


if __name__== '__main__':
  main()