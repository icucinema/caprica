#!/usr/bin/env python
# coding: utf-8

from base import CapricaDevice

UUID='8b6eab2f-2c9c-4910-9fb4-543c653c7b04'

class TestDevice(CapricaDevice):
  pass

if __name__ == '__main__':
  t = TestDevice(UUID)
  t.run()
