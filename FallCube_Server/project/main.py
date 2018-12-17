import os
import sys

from file_transfer.file_transfer import FileTransfer

# Main entry point
def main():
    # Ensure valid usage
    if len(sys.argv) < 4 or sys.argv[1] == '-h' or not sys.argv[3].isnumeric():
        print("Usage:", os.path.basename(__file__), "download_dir server_path server_port\n")
      
        return 

    file_transfer = FileTransfer(sys.argv[1], sys.argv[2], sys.argv[3])
    file_transfer.run()
    file_transfer.close()

if __name__== '__main__':
  main()