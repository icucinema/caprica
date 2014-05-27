#!/usr/bin/env python
# coding: utf-8

from base import CapricaDevice, CapricaRequestHandler

class ButtonHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.state['button']))

  def put(self):
    self.dev.state['button'] = self.get_argument("state").lower() == "true"


class TestDevice(CapricaDevice):
  routes = {r"/api/button": ButtonHandler}
  state = {"button": False}

if __name__ == '__main__':
  t = TestDevice()
  t.run()
