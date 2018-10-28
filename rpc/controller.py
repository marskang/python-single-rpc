# -*- coding: utf-8 -*-

from google.protobuf.service import RpcController


class Controller(RpcController):

    def __init__(self):
        self.is_reset = False
        self.is_failed = False
        self.error_text = ""
        self.is_cancelled = False
        self.cancel_callback = None


    def Reset(self):
        print('reset ' * 10)
        return self.is_reset


    def Failed(self):
        print('failed' * 10)
        raise self.is_failed


    def ErrorText(self):
        print('error_text' * 10)
        return self.error_text


    def StartCancel(self):
        print('start cancel ' * 10)
        self.is_cancelled = True


    def SetFailed(self, reason):
        print('set_failed ' * 10)
        self.is_failed = True
        self.error_text = reason


    def IsCanceled(self):
        print('is canceled ' * 10)
        raise self.is_cancelled


    def NotifyOnCancel(self, callback):
        print('notify on cancle' * 10)
        self.cancel_callback = callback
