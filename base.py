# coding: utf-8
from twisted.application import internet, service
from twisted.internet import reactor, task, protocol
import cyclone.sse
import cyclone.web
from existence import *

MAX_TTL = 2
EXPUNGE_INTERVAL = 7
API_PORT = 56789

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
    t = reactor.listenUDP(EXISTENCE_PORT, protocol)
    l = task.LoopingCall(self.expungeLostDevices)
    l.start(EXPUNGE_INTERVAL)
    reactor.run()

class ApiApplication(cyclone.web.Application):
  def __init__(self, apiRoutes):
    handlers = [(r"/updates", DevUpdateHandler)] + apiRoutes
    settings = dict(debug=True)
    cyclone.web.Application.__init__(self, handlers, **settings)

class DevUpdateHandler(cyclone.sse.SSEHandler):
  clients = []

  def bind(self):
    print "Got client" + client
    self.clients.append(client)

  def unbind(self):
    print "Lost client" + client
    self.clients.remove(client)

  def broadcast(self, message):
    for client in self.clients:
      try:
        client.sendEvent(message)
      except:
        #TODO: error handling?
        print "Failed to send message"

class CapricaRequestHandler(cyclone.web.RequestHandler):
  def __init__(self, request, *args, **kwargs):
    self.dev = kwargs.pop('dev')
    super(CapricaRequestHandler, self).__init__(request, *args, **kwargs)

class CapricaDevice(object):
  def __init__(self, uuid):
    self.uuid = uuid

  def sayHi(self, proto):
    proto.sayHi(self.uuid)

  def run(self):
    protocol = DeviceExistenceProtocol(self, EXISTENCE_PORT, self.uuid)
    broadcastPort = reactor.listenUDP(0, protocol)

    routeList = [(key, value, dict(dev=self)) for (key, value) in self.routes.iteritems()]
    apiApp = ApiApplication(routeList)
    apiPort = reactor.listenTCP(API_PORT, apiApp)
    reactor.run()
