# -*- coding: utf-8 -*-

import struct
import asyncio
import traceback
from protos.rpc_pb2 import Packet
from service import MyEchoService
from controller import Controller

LENGTH_HEADER = '!I'
HEADER_LENGTH = struct.calcsize(LENGTH_HEADER)


def handle_request(service, data):
    packet = Packet()
    packet.ParseFromString(data)
    _descriptor = service.GetDescriptor()
    method = _descriptor.methods[packet.method_id]
    request = service.GetRequestClass(method)()
    request.ParseFromString(packet.content)
    controller = Controller()
    return service.CallMethod(method, controller, request, send_response_callback)


def send_response_callback(response):
    return response.SerializeToString()


class Server(object):

    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8888

    async def read_packet(self, reader):
        b_len = await reader.readexactly(HEADER_LENGTH)
        (packet_len,) = struct.unpack(LENGTH_HEADER, b_len)
        data = await reader.readexactly(packet_len)
        return data

    async def accept(self, reader, writer):
        try:
            while True:
                packet_data = await self.read_packet(reader)
                service = MyEchoService()
                resp = handle_request(service, packet_data)
                packet_len = struct.pack(LENGTH_HEADER, len(resp))
                writer.write(packet_len + resp)
                await writer.drain()
        except Exception:
            traceback.print_exc()
        finally:
            writer.close()

    def start(self):
        loop = asyncio.get_event_loop()
        server_coro = asyncio.start_server(self.accept, self.ip, self.port, loop=loop)
        server = loop.run_until_complete(server_coro)
        try:
            loop.run_forever()
        finally:
            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()

s = Server()
s.start()