#!/usr/bin/env python
# coding: utf-8

from base import CapricaDevice, CapricaRequestHandler

class MuteHandler(CapricaRequestHandler):
  def get(self):
    self.dev.state[]

class ButtonHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.state['button']))

  def put(self):
    self.dev.state['button'] = self.get_argument("state").lower() == "true"


class CP500Device(CapricaDevice):
  routes = { r"/api/mute"   : MuteHandler,
             r"/api/volume" : VolumeHandler,
             r"/api/source" : SourceHandler }
  state = {"mute": False, "volume": 0, "source": ""}

  def __init__(self):
    super(TestDevice, self).__init__()


  HEADER   = [0x55, 0xaa]
  ADDR_CP500  = [0]
  ADDR_REMOTE = [1]
  ADDR_
  SEND     = [0]
  RECV     = [1]
  PKT_LEN  = 6
  BTN_SEND = [0]
  BTN_RECV = [8]
  VOL      = [1]
  UP       = [1]
  DOWN     = [0]

  def makeChecksum(packet):
    return [0xff-(sum(packet) % 0x100)]

  def makeChecksumPacket(packet):
    return packet + makeChecksum(packet)

  def makeButtonPacket(button):
    return makeChecksumPacket(HEADER + SEND + VOL_UP)

  def makeVolPacket(direction):
    return makeChecksumPacket(HEADER + VOL + direction)

if __name__ == '__main__':
  t = TestDevice()
  t.run()
