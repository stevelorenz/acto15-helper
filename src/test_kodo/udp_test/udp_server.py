#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   : 2015-12-28 09:50:27
# About  : Recieve RLNC coded packets using kodo
# #############################################################################

import socket
import kodo

###############################################################################
# Init RLNC Decoder
###############################################################################

symbols = 20  # generation size
symbol_size = 2  # the symbol_size in bytes

# init full RLNC decoder use GF(2)
decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)
decoder = decoder_factory.build()

###############################################################################
# Recieve coded packets using UDP
###############################################################################

UDP_IP = ""  # recieve from all ip address
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_PORT))

# if the decoding is not finish
while not decoder.is_complete():
    packet, addr = sock.recvfrom(1024)
    r = decoder.rank()
    print("the rank is %d" % r)
    decoder.read_payload(packet)

# get the decoded data from decoder
data_out = decoder.copy_from_symbols()
print("the decoded data is %s" % data_out)
