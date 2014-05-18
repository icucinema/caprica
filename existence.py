# coding: utf-8
from twisted.internet import task
from twisted.internet.protocol import DatagramProtocol

PORT = 8555
BROADCAST_INTERVAL = 5

class DeviceExistenceProtocol(DatagramProtocol):
  def __init__(self, controller, port, uuid):
    self.uuid = uuid

  def startProtocol(self):
    self.transport.setBroadcastAllowed(True)
    self._call = task.LoopingCall(self.sayHi)
    self._loop = self._call.start(BROADCAST_INTERVAL)

  def stopProtocol(self):
    self._call.stop()

  def sayHi(self):
    hiMsg = "HELO " + self.uuid;
    self.transport.write(hiMsg, ('<broadcast>', PORT))
    print "broadcast"

class DeviceExistenceProtocolListener(DatagramProtocol):
  def __init__(self, controller):
    self.controller = controller

  def datagramReceived(self, datagram, host):
    self.controller.processDatagram(datagram, host)
