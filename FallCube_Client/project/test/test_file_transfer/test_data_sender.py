import pytest
import socket
from threading import Thread

from file_transfer.data_sender import DataSender

def setup_socket():
    """
    Setup fake server
    """

    sock = socket.socket()
    sock.bind(('127.0.0.1', 12345))
    sock.listen(5)
    
    client, _ = sock.accept()
    data = client.recv(1024).decode()
    if data == 'test':
        client.send('ok'.encode())
    else:
        client.send('err'.encode()) # Will cause client to fail with OSError exception 

    client.close()
    sock.close()


def test_connect_success():
    """
    Test simple connection, notify and response listening of DataSender
    """

    t = Thread(target=setup_socket)
    t.start()

    data_sender = DataSender('127.0.0.1', 12345)
    server_response = data_sender.notify('test')

    assert server_response == 'ok'

    data_sender.close()
    t.join()

def test_connect_fail():
    with pytest.raises(OSError):
        """
        Test DataSender's handeling of unexpected message from server
        """

        t = Thread(target=setup_socket)
        t.start()

        data_sender = DataSender('127.0.0.1', 12345)
        data_sender.notify('bad message')

        data_sender.close()
        t.join()    