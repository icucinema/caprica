# coding: utf-8

from twisted.application import internet, service
from twisted.internet import reactor, task
from existence import *

MAX_TTL = 2
EXPUNGE_INTERVAL = 7

class CapricaControlPoint:
  def __init__(self):
    self.known_devices = {}

  def expungeLostDevices(self):
    for uuid,info in self.known_devices.items():
      info['ttl'] -= 1
      if info['ttl'] == 0:
        del self.known_devices[uuid]
        print "Lost device " + uuid

  def processDatagram(self, datagram, (host, port)):
    cmd = datagram.split(' ')
    if cmd[0] == "HELO":
      uuid = cmd[1]
      if uuid not in self.known_devices:
        self.known_devices[uuid] = {'host': host, 'port': port, 'ttl': MAX_TTL}
        print "Found new device " + uuid
      else:
        self.known_devices[uuid]['ttl'] = MAX_TTL

  def run(self):
    protocol = DeviceExistenceProtocolListener(self)
    t = reactor.listenUDP(PORT, protocol)
    l = task.LoopingCall(self.expungeLostDevices)
    l.start(EXPUNGE_INTERVAL)
    reactor.run()

class CapricaDevice:
  def __init__(self, uuid):
    self.uuid = uuid

  def sayHi(self, proto):
    proto.sayHi(self.uuid)

  def run(self):
    protocol = DeviceExistenceProtocol(self, PORT, self.uuid)
    t = reactor.listenUDP(0, protocol)
    reactor.run()
