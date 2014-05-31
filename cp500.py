#!/usr/bin/env python
# coding: utf-8

from base import CapricaDevice, CapricaRequestHandler
import serial

CP500_SERIAL_PORT = '/dev/ttyUSB0'

class MuteHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.state['mute']))

  def put(self):
    self.dev.state['mute'] = self.get_argument("state").lower() == "true"

    resp = self.dev.cmdAndResp(self.dev.makeButtonPacket('Mute'))
    if resp[3] != self.dev.MUTE_RECV
      raise Exception("not a mute update event")

    #Ensure the CP500 matches our internal state, if not flip it again, as we must
    #have started in an inconsistent state
    newState = resp[4]
    if bool(newState) != self.dev.state['mute']:
      self.dev.cmdAndResp(self.dev.makeButtonPacket('Mute'))

class SourceHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.state['source']))

  def put(self):
    self.dev.state['source'] = self.get_argument('source').lower()

    resp = self.dev.cmdAndResp(self.dev.makeButtonPacket(self.dev.SOURCE_MAP.get(self.dev.state['source'], 0)))
    if resp[3] != self.dev.BTN_RECV:
      raise Exception("not a format led change event")

   #TODO: care about the response more?

class VolumeHandler(CapricaRequestHandler):
  def get(self):
    self.write(str(self.dev.state['volume']))

  def put(self):
    self.dev.state['volume'] = float(self.get_argument('volume'))
    self.dev.setToVolume(self.dev.state['volume'])

class CP500Device(CapricaDevice):
  routes = { r"/api/mute"   : MuteHandler,
             r"/api/volume" : VolumeHandler,
             r"/api/source" : SourceHandler }
  state = {"mute": False, "volume": 0, "source": ""}

  def __init__(self):
    self.serial = serial.Serial(CP500_SERIAL_PORT, 9600, timeout=5, bytesize=8, parity='N', stopbits=1)
    super(TestDevice, self).__init__()

  BTN_MAP =  {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 'Mute': 0xd}
  SOURCE_MAP = {'cd': 1, 'digital':3, 'pc':4, '35mm': 8}
  PKT_LEN   = 6
  HEADER   = [0x55, 0xaa]
  ADDR_CP500  = [0]
  ADDR_REMOTE = [1]
  SEND      = [0]
  RECV      = [1]
  BTN_SEND  = [0]
  BTN_RECV  = [8]
  MUTE_RECV = [9]
  VOL       = [1]
  7SEG_RECV = [7]
  UP        = [1]
  DOWN      = [0]

  def cmdAndResp(cmd):
    self.serial.write(bytearray(cmd))
    resp = self.serial.read(self.PKT_LEN)
    if resp[0,2] != self.HEADER
      raise Exception("invalid header?")
    if resp[2] != [self.RECV]
      raise Exception("not a receipt packet!")
    if self.makeChecksum(resp[0, 5]) != resp[5]
      raise Exception("checksum mismatch")
    return resp

  def makeChecksum(packet):
    return [0xff-(sum(packet) % 0x100)]

  def makeChecksumPacket(packet):
    return packet + self.makeChecksum(packet)

  def makeButtonPacket(button):
    return self.makeChecksumPacket(self.HEADER + self.SEND + self.BTN_SEND + self.BTN_MAP.get(button, 0xff))

  def makeVolPacket(direction):
    return self.makeChecksumPacket(self.HEADER + self.VOL + direction)

  def setToVolume(target):
    #As we can only do +0.1, -0.1 we need to work a bit here

    #First, issue a single down to get the current volume
    resp = self.cmdAndResp(self.makeVolPacket(self.DOWN))
    if resp[3] != self.dev.7SEG_RECV:
      raise Exception("not a volume change event")
    curLevel = float(resp[4])

    #Now, work out direction and distance to travel
    if curLevel == target:
      return
    direction = self.UP if target > curLevel else self.DOWN
    steps = int(round(abs(target - curLevel), 1) * 10)

    #Now send that many vol changes
    for i in range(0, steps+1):
      self.cmdAndResp(self.makeVolPacket(direction))

if __name__ == '__main__':
  t = TestDevice()
  t.run()
