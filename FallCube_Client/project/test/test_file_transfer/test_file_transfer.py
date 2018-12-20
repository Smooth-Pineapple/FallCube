import os
import pytest
import socket
from threading import Thread
from pyfakefs.fake_filesystem_unittest import Patcher

from file_transfer.file_transfer import FileTransfer

import time

@pytest.fixture
def fake_filesystem(fs):
    """
    Set up fake filesystem
    """

    fs.create_file('FAKE FILE.txt', contents='hello')

def setup_socket():
    """
    Setup fake server
    """
    
    sock = socket.socket() 
    sock.bind(('127.0.0.1', 12345)) 
    sock.listen(5)

    client, _ = sock.accept()
    data = client.recv(1024).decode()
    
    if data == 'test|handle response|' + os.sep + 'FAKE FILE.txt':
        client.send('ok'.encode())
    elif data == 'test|handle err silently|' + os.sep + 'FAKE FILE.txt':
        client.send('err'.encode()) # Will cause client to fail with socket.error exception so test  should handle this exception 
    else:
        return
    

    client.close()
    sock.close()

def test_msg_success(fake_filesystem):
    """
    Test simple successful connection and receiving of message
    """

    t = Thread(target=setup_socket)
    t.start()

    file_transfer = FileTransfer('.', '127.0.0.1', 12345)
    file_transfer.transfer('test|handle response', '', 'FAKE FILE.txt' )
    
    t.join()

def test_error_handle(fake_filesystem):
    """
    Test quiet handling of error
    """

    t = Thread(target=setup_socket)
    t.start()

    file_transfer = FileTransfer('', '127.0.0.1', 12345)
    file_transfer.transfer('test|handle err silently', '', 'FAKE FILE.txt')

    t.join()
