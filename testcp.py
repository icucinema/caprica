#/usr/bin/env python
#coding: utf-8

from twisted.application import internet, service
from twisted.internet import reactor
from existence import *

class DeviceExistenceListener:
  def processDatagram(self, datagram, (host, port)):
    print "recv'd " + datagram + " from " + host + ":" + str(port)

  def run(self):
    protocol = DeviceExistenceProtocolListener(self)
    t = reactor.listenUDP(PORT, protocol)
    reactor.run()

if __name__ == '__main__':
  DeviceExistenceListener().run()
