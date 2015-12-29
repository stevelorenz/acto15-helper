#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ###################################################################################
# About  : Project of course actual topics 2015
#          Simulate a topology where an encoder broadcasts packets to the decoder
#          and a helper node
# Author : Xiang,Zuo
# Email  : xianglinks@gmail.com
# Date   : 2015-12-29 18:21:13
# ###################################################################################

import os
import numpy as np
import random
import sys

import kodo


def main():
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

    # init the the generation size in RLNC
    # and the size of a symbol in bytes
    symbols = 100  # the generation size
    symbol_size = 1500  # usually the MTU of the network 1400 - 1600 bytes

    # init error probabilities e_1, e_2, e_3
    # suppose that e_1 = e_2 (symmetrical)
    e_1 = e_2 = 0.2
    e_3 = 0.6

    # TODO: (optional) parameterize different encoders/decoders
    # firstly use a Full RLNC coder with GF(2) Field
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    encoder = encoder_factory.build()

    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    recoder = decoder_factory.build()
    decoder = decoder_factory.build()

    # create some data to encode. In this case we make a buffer
    # with the same size as the encoder's block size (the max.
    # amount a single encoder can encode) -> block_size = symbols * symbol_size
    # fill the input data with random data using /dev/urandom
    data_in = os.urandom(encoder.block_size())

    # put the data buffer to the encoder so that we may start to produce encoded symbols from it
    #  encoder.set_const_symbols(data_in)  # TODO: this is not support by my current compiled version of kodo
    encoder.set_symbols(data_in)

    # init counters for each node
    ct_encoder_sent = 0  # packets sent from encoder
    ct_recoder_sent = 0  # packets sent from recoder
    ct_recoder_recv = 0  # packets recieved by recoder
    ct_decoder_recv = 0  # packets recieved by decoder
    ct_recoder_deco = 0  # packets decoded by recoder

    """
    threshold value of decoded packets by recoder before starting send packets
    the rank value of the recoder play a important role here
    """
    threshold_recoder = symbols + 1
    threshold_recoder = 10

    print("the threshold of recoder is %d" % threshold_recoder)

    flag = 0  # flag for alternatively sending by encoder and recoder

    # main loop: until the decoder has decoded all the orginal packets
    # systematic coding should be firstly tested
# -------------------------------------------------------------------------------------------------
    while not decoder.is_complete():
        # select either encoder or recoder as packet source
        # here is determined by the number of decoded packets by recoder

        # only encoder send packets, the recoder keep gathering packets
        if ct_recoder_deco < threshold_recoder:
            # the encoder send a packet
            packet = encoder.write_payload()
            ct_encoder_sent += 1

            # broadcast the packet from the encoder
            # both recoder and decoder try to recieve the packet
            if np.random.uniform(0, 1) > e_1:
                # the recoder get the packet
                recoder.read_payload(packet)
                ct_recoder_recv += 1
                ct_recoder_deco = recoder.rank()  # update the number of decoded packets in recoder

            if np.random.uniform(0, 1) > e_3:
                # the decoder get the packet
                decoder.read_payload(packet)
                ct_decoder_recv += 1

        # the helper start to send packets(if ct_recoder_deco >= threshold_recoder)
        # test-scenario1: the encoder and recoder send packets alternatively
        else:
            # recoder send a packet
            if flag == 0:
                packet = recoder.write_payload()
                ct_recoder_sent += 1

                # only the decoder try to get the packet
                if np.random.uniform(0, 1) > e_2:
                    decoder.read_payload(packet)
                    ct_decoder_recv += 1

                flag = not flag  # change flag for next round

            # encoder sent a packet
            else:
                packet = encoder.write_payload()
                ct_encoder_sent += 1

                # broadcast the packet from the encoder
                # both recoder and decoder try to recieve the packet

                if np.random.uniform(0, 1) > e_1:
                    recoder.read_payload(packet)
                    ct_recoder_recv += 1
                    ct_recoder_deco = recoder.rank()  # update the decoded packets in recoder

                if np.random.uniform(0, 1) > e_3:
                    decoder.read_payload(packet)
                    ct_decoder_recv += 1

                flag = not flag  # change flag for next round
# -------------------------------------------------------------------------------------------------

    # after main loop:
    # TODO: count linear dependent packets by packet source
    # count total packets sent
    total_packets_sent = ct_encoder_sent + ct_recoder_sent

    # copy the symbols from the decoders
    data_out = decoder.copy_from_symbols()

    # check we properly decoded the data
    if data_out == data_in:
        print("data decoded correctly...")
        print("packets sent from encoder is %d" % ct_encoder_sent)
        print("packets recieved by recoder is %d" % ct_recoder_recv)
        print("packets decoded by recoder is %d" % ct_recoder_deco)
        print("packets sent from recoder is %d" % ct_recoder_sent)
        print("packets recieved by decoder is %d" % ct_decoder_recv)
        print("total number packets sent is %d" % total_packets_sent)

    else:
        print("unexpected failure to decode please file a bug report :)")
        sys.exit(1)

if __name__ == "__main__":
    main()
