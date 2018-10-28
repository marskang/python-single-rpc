# -*- coding: utf-8 -*-

import struct
import traceback
from google.protobuf.service import RpcChannel
from google.protobuf.service import RpcController
from protos.rpc_pb2 import Packet


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

class Channel(RpcChannel):

    def __init__(self, service, conn):
        super(Channel, self).__init__()
        self.service = service
        self.controller = RpcController()
        self.conn = conn

    def CallMethod(self, method_descriptor, rpc_controller,
                   request, response_class, done):
        service_descriptor = method_descriptor.containing_service
        service_id = service_descriptor.index
        method_id = method_descriptor.index
        data = request.SerializeToString()
        packet = Packet()
        packet.service_id = service_id
        packet.method_id = method_id
        packet.content = data
        packet_data = packet.SerializeToString()
        packet_len = struct.pack(LENGTH_HEADER, len(packet_data))
        self.conn.sendall(packet_len+packet_data)
        b_len = recv_fill(self.conn, HEADER_LENGTH)
        (packet_len,) = struct.unpack(LENGTH_HEADER, b_len)
        data = recv_fill(self.conn, packet_len)
        resp = response_class()
        resp.ParseFromString(data)
        return resp