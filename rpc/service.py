# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, '../')

from protos.echo_pb2 import EchoService


class MyEchoService(EchoService):

    def echo(self, controller, request, done):
        print('echo echo')
        print(request)
        print(type(request))
        return done(request)