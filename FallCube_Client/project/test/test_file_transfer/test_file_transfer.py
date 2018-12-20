import os
import pytest
import socket
from threading import Thread
from pyfakefs.fake_filesystem_unittest import Patcher

from file_transfer.file_transfer import FileTransfer

@pytest.fixture
def fake_filesystem(fs):
    """
    Set up fake filesystem
    """

    fs.create_file('FAKE FILE.txt', contents='hello')

import threading

class ExcThread(threading.Thread):
  def excRun(self):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 12345))
    sock.listen(5)
    sock.timeout(10)
    
    client, _ = sock.accept()
    data = client.recv(1024).decode()

    if data == 'test|' + os.sep + 'FAKE FILE.txt':
        client.send('read'.encode())
        while data:
            data = client.recv(1024)
            if 1 == 1:
                raise Exception('Expected FAKE FILE.txt to contain "Hello"')
    elif data == 'test':
         client.send('ok'.encode())   
    else:
        client.send('err'.encode()) # Will cause client to fail with OSError exception 

    client.close()
    sock.close()

  def run(self):
    self.exc = None
    try:
      # Possibly throws an exception
      self.excRun()
    except:
      import sys
      self.exc = sys.exc_info()
      # Save details of the exception thrown but don't rethrow,
      # just complete the function

  def join(self):
    threading.Thread.join(self)
    if self.exc:
      msg = "Thread '%s' threw an exception: %s" % (self.getName(), self.exc[1])
      new_exc = Exception(msg)
      raise new_exc.with_traceback(self.exc[2])

def setup_socket(num_connections, time_out):
    """
    Setup fake server
    """

    sock = socket.socket()
    sock.bind(('127.0.0.1', 12345))
    sock.listen(num_connections)
    sock.timeout(time_out)
    
    client, _ = sock.accept()
    print('ASDASDSA')
    data = client.recv(1024).decode()

    print('woiehrf')
    if data == 'test|' + os.sep + 'FAKE FILE.txt':
        print('AAAA')
        client.send('read'.encode())
    elif data == 'test read|' + os.sep + 'FAKE FILE.txt':
        print('HELLO')
        client.send('ok'.encode())  
        print('WORLS')
        while data:
            data = client.recv(1024)
        print('sAS')
    else:
        print('ssssAS')
        client.send('err'.encode()) # Will cause client to fail with OSError exception 

    client.close()
    sock.close()


def test_msg_success(fake_filesystem):
    """
    Test simple successful connection
    """

    t = Thread(target=setup_socket, args=(5, 10))
    t.start()

    file_transfer = FileTransfer('.', '127.0.0.1', 12345)
    file_transfer.transfer('test', '', 'FAKE FILE.txt' )
    
    t.join()


def test_read_success():
    """
    Test read and data transfer capabilities
    """

    #t = Thread(target=setup_socket, args=(5, 10))
    t = ExcThread()
    t.start()
    try:
        file_transfer = FileTransfer('', '127.0.0.1', 12345)
        file_transfer.transfer('test read', '', 'FAKE FILE.txt' )
    except Exception as e:
        raise pytest.fail(e)

    
    t.join()
 