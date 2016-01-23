#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# #####################################
# About  : Project of course actual topics 2015
#          Simulate a topology where an encoder broadcasts packets to the decoder
#          and a helper node
# Author : Xiang,Zuo
# Email  : xianglinks@gmail.com
# Date   : 2016-01-03 18:01:24
# #####################################

import os

import numpy as np

from helper_test import simulate


"""
This example simulates a topology where an encoder broadcasts packets to
the decoder and a helper node. The helper node can support the encoder by
sending additional packets to the decoder.  But in each step of the
simulation either only encoder or helper can generate a packet.(compete for
the access to the wireless channel). If the helper cannot provide new info, it
it just stealing the sending time of original encoder

                             +-----------+
                   __________|  helper   |__________
                  /    e_1   | (recoder) |   e_2    \
                 /           +-----------+           \
          +-----------+                         +-----------+
          |  encoder  |-------------------------|  decoder  |
          +-----------+           e_3           +-----------+
"""


def main():
    print("Simulation started...")
    # init the the generation size in RLNC and the size of a symbol in bytes
    symbols = 100  # the generation size
    symbol_size = 1500  # usually the MTU of the network 1400 - 1600 bytes

    # init error probabilities e_1, e_2, e_3
    # suppose that e_1 = e_2 (symmetrical)
    e_1 = e_2 = 0.9

    open('./results.dat', 'w').close()  # empty the data in file

    # loop for different e_3
    for e_3 in np.arange(0, 1, 0.05):

        """
         threshold_recoder(tr): number of transmission from the sender before the helper starts transmitting
         according to the PlayNCool policy :
         tr = -g * C(e) / D(e) - (1 - e_3 ) * C(e)
         with C(e) = (-1 + e_2 + e_3 - e_1 * e_3)
              D(e) = (2 - e_3 - e_2) * (e_3 - e_1 * e_3)
        """
        C = (-1 + e_2 + e_3 - e_1 * e_3)
        D = (2 - e_3 - e_2) * (e_3 - e_1 * e_3)
        tr = (-1 * symbols * C) / (D - (1 - e_3) * C)
        tr = int(tr)
        #  print("the threshold of recoder is %d" %tr)

        # init data to be transmitted
        # fill the input data with random data using /dev/urandom
        data_in = os.urandom(symbols * symbol_size)

        # Simulation ----------------------------------------------------------------------
        num_sim = 50  # number of simulations each round

        # 1.simulation without the helper
        #  print("the result without helper:")
        simulate(symbols, symbol_size, e_1, e_2, e_3, symbols * 100, data_in, num_sim)
        #  print("the result with helper using PlayNCool:")
        # 2.simulation with helper using PlayNCool policy(in region2)
        simulate(symbols, symbol_size, e_1, e_2, e_3, tr, data_in, num_sim)

    print("Simulation finished. results in ./results.dat")

if __name__ == "__main__":
    main()
