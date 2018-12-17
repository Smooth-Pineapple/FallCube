import os
import sys

from file_tracking.file_tracking import FileTracking
from file_tracking.monitor import Monitor
from file_tracking.scan_once import ScanOnce

from file_reader.file_reader import FileReader

def printD(event, dir, file):
    #created
    #deleted
    #modified 
    #move
    if file != '':
        file_to_parse = FileReader.from_path('C:/Users/dudeman3000/Documents/Python/FallCube/FallCube_Client/Test_Input_Dir'+dir+'/'+file, 1024)
        if file_to_parse != None:
            r = file_to_parse.init_read()
            while r:
                print('Sent ',repr(r))
                r = file_to_parse.read()
            file_to_parse.close()
    print(event, dir, file)

# Main entry point
def main():
    # Ensure valid usage
    if len(sys.argv) < 3 or sys.argv[1] == '-h':
        print("Usage:", os.path.basename(__file__), "monitor_dir server_path server_port\n")
      
        return 

    file_tracker = [ScanOnce(sys.argv[1], printD), Monitor(sys.argv[1], printD)]
    for tracker in file_tracker:
        tracker.run()

    # parse dir
    # send each file to serv
    # monitor dir
        # send each new to serv


if __name__== '__main__':
  main()