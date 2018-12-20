import os
import pytest
import socket
import time

from threading import Thread
from pyfakefs.fake_filesystem_unittest import Patcher

from file_transfer.file_transfer import FileTransfer


@pytest.fixture
def fake_filesystem(fs):
    """
    Set up fake filesystem
    """

    fs.create_dir('a')
    fs.create_file('f1.txt')
    fs.create_dir('c' + os.sep + 'f2.txt')
    fs.create_dir('c' + os.sep + 'd')

    return fs

@pytest.fixture(scope='module')
def file_transfer(request):
    """
    Manage a FileTransfer object on a thread 
    """

    file_transfer = FileTransfer('', '127.0.0.1', 12345)    
    file_transfer.start()

    def end():
        file_transfer.close()

    request.addfinalizer(end)      

@pytest.fixture
def setup_client(request):
    """
    Create basic client
    """

    client = socket.socket()
    client.settimeout(5)
    client.connect(('127.0.0.1', 12345))

    def end():
        client.close()


    request.addfinalizer(end)

    return client


def test_run_create_file_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to good file creation message
    """

    setup_client.send('created|file|f2.txt'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'read'

    setup_client.send(b'hello')
    assert os.path.exists('f2.txt')
    

def test_run_create_file_fail(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to bad file creation message
    """

    setup_client.send('created|file|f1.txt'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'end'

    
def test_run_create_dir_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to good directory creation message
    """

    setup_client.send('created|dir|b'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'create'

    time.sleep(2) # Takes a moment to create
    assert os.path.exists('b')


def test_run_create_dir_fail(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to bad directory creation message
    """

    setup_client.send('created|dir|a'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'end'

def test_run_delete_file_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to file deletion message
    """

    setup_client.send('deleted|f1.txt'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'remove'

    time.sleep(2) # Takes a moment to delete
    assert not os.path.exists('f1.txt')

def test_run_delete_dir_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to directory deletion message
    """

    setup_client.send('deleted|a'.encode())

    response = setup_client.recv(1024).decode()
    assert response == 'remove'

    time.sleep(2) # Takes a moment to delete
    assert not os.path.exists('a')

def test_run_move_file_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to renaming a file message
    """

    setup_client.send(('moved|file|c' + os.sep + 'f3.txt|c' + os.sep +  'f2.txt').encode())

    response = setup_client.recv(1024).decode()
    assert response == 'rename'

    time.sleep(2) # Takes a moment to delete/ create
    assert os.path.exists('c' + os.sep + 'f3.txt')
    assert not os.path.exists('c' + os.sep + 'f2.txt')

def test_run_move_dir_success(fake_filesystem, file_transfer, setup_client):
    """
    Test server response to renaming a directory message
    """

    setup_client.send(('moved|dir|c' + os.sep + 'e|c' + os.sep +  'd').encode())

    response = setup_client.recv(1024).decode()
    assert response == 'rename'

    time.sleep(2) # Takes a moment to delete/ create
    assert os.path.exists('c' + os.sep + 'e')
    assert not os.path.exists('c' + os.sep + 'd')