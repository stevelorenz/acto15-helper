#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   : 2015-12-28 09:50:27
# About  : Send RLNC coded packets using kodo
# #############################################################################

import socket
import kodo

###############################################################################
# Init RLNC Encoder
###############################################################################

symbols = 20  # the generation size
symbol_size = 2  # the symbol size in bytes

# init full RLNC encoder use GF(2)
encoder_factory = kodo.FullVectorEncoderFactoryBinary(symbols, symbol_size)
encoder = encoder_factory.build()

###############################################################################
# Send coded packets using UDP
###############################################################################

UDP_IP = '127.0.0.1'
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = 'hello my name is xiang zuo'

messLen = len(message)
print "the length of message is %d" % messLen

encoder.set_symbols(message)

for i in range(22):
    packet = encoder.write_payload()
    sock.sendto(packet, (UDP_IP, UDP_PORT))

print("packet sending finished...")
