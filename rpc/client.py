# -*- coding: utf-8 -*-

import socket
import struct
import traceback

from protos.echo_pb2 import Msg
from protos.echo_pb2 import EchoService
from protos.echo_pb2 import EchoService_Stub
from channel import Channel
from controller import Controller

s = socket.socket()
LENGTH_HEADER = '!I'

HEADER_LENGTH = struct.calcsize(LENGTH_HEADER)


def recv_fill(sock, packet_len):
    buff = b''
    while len(buff) < packet_len:
        try:
            data = sock.recv(packet_len - len(buff))
            if not data:
                return None
            buff += data
        except Exception as e:
            traceback.print_exc()
            return None
    return buff


def main():
    host = '127.0.0.1'
    port = 8888
    s.connect((host, port))
    service = EchoService()
    channel = Channel(service, s)
    stub = EchoService_Stub(channel)
    controller = Controller()
    msg = Msg()
    msg.text = '第一次调用echo'
    resp = stub.echo(controller, msg)
    print('frist call resp:',resp.text)
    msg.text = '第二次调用echo'
    resp = stub.echo(controller, msg)
    print('second call resp:', resp.text)
    s.close()

if __name__ == '__main__':
    main()