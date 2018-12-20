import pytest
import socket
from threading import Thread

from file_transfer.data_receiver import DataReceiver


@pytest.fixture
def setup_data_receiver():
    data_receiver = DataReceiver('127.0.0.1', 12345)
    data_receiver.connect()

    return data_receiver


def test_data_receiver(setup_data_receiver):
    """
    Test simple connection, communication and closure of server
    """

    client = socket.socket()
    client.settimeout(60)
    client.connect(('127.0.0.1', 12345))

    assert client.send(b'hello') == 5

    client.close()
    setup_data_receiver.close()
