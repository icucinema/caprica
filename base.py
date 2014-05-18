# coding: utf-8

from twisted.application import internet, service
from twisted.internet import reactor
from existence import *

class CapricaControlPoint:
  def __init__(self):
    self.known_devices = {}

  def processDatagram(self, datagram, (host, port)):
    cmd = datagram.split(' ')
    if cmd[0] == "HELO":
      uuid = cmd[1]
      if not (uuid in self.known_devices):
        self.known_devices[uuid] = {'host': host, 'port': port, 'ttl': 5}
        print "Found new device " + uuid

  def run(self):
    protocol = DeviceExistenceProtocolListener(self)
    t = reactor.listenUDP(PORT, protocol)
    reactor.run()

class CapricaDevice:
  pass
