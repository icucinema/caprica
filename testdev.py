#!/usr/bin/env python
# coding: utf-8
# twistd -ny testdev.py

from twisted.application import internet, service
from twisted.internet import reactor
from existence import *

UUID='8b6eab2f-2c9c-4910-9fb4-543c653c7b04'

class DeviceExistenceAdvertiser:
  def sayHi(self, proto):
    proto.sayHi(UUID)

  def run(self):
    protocol = DeviceExistenceProtocol(self, PORT, UUID)
    t = reactor.listenUDP(0, protocol)
    reactor.run()

if __name__ == '__main__':
  DeviceExistenceAdvertiser().run()
