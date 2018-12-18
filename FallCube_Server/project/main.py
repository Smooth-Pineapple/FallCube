import os
import sys

from file_transfer.file_transfer import FileTransfer

# Main entry point
def main():
    # Ensure valid usage
    if len(sys.argv) < 4 or sys.argv[1] == '-h' or not sys.argv[3].isnumeric():
        print("Usage:", os.path.basename(__file__), "sync_to_dir server_path server_port\n")
      
        return 
    try:
        if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
            if os.listdir(sys.argv[1]):
                print("Must provide empty directory!")
                return
        else:
            print("Directory does not exist, so will make it")
            os.makedirs(sys.argv[1])
    except OSError as e:
        print("OSError error:", e)
        
    file_transfer = FileTransfer(sys.argv[1], sys.argv[2], sys.argv[3])
    file_transfer.run()
    file_transfer.close()

if __name__== '__main__':
  main()