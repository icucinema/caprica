#!/usr/bin/env python
# coding: utf-8

from base import CapricaDevice, CapricaRequestHandler

UUID='8b6eab2f-2c9c-4910-9fb4-543c653c7b04'


class ButtonHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.buttonState))

  def put(self):
    global buttonState
    self.dev.buttonState = self.get_argument("state").lower() == "true"


class TestDevice(CapricaDevice):
  routes = {r"/api/button": ButtonHandler}

  def __init__(self, uuid):
    super(TestDevice, self).__init__(uuid)

    self.buttonState = False

if __name__ == '__main__':
  t = TestDevice(UUID)
  t.run()
