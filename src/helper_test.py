#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ###################################################################################
# Date   : 2015-12-29 11:48:49
# About  : Simulate a topology where an encoder broadcasts packets to the decoder
#          and a helper node
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

    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    # TODO: parameterize symbols per generation
    symbols = 42  # the generation size
    symbol_size = 1400  # usually the MTU of the network 1400 - 1600 bytes

    # TODO: parameterize error probabilities e_1, e_2, e_3
    # suppose that e_1 = e_2
    e_1 = e_2 = 0.1
    e_3 = 0.4

    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders

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

    # Create some data to encode. In this case we make a buffer
    # with the same size as the encoder's block size (the max.
    # amount a single encoder can encode) -> block_size = symbols * symbol_size
    # fill the input data with random data
    data_in = os.urandom(encoder.block_size())

    # put the data buffer to the encoder so that we may start
    # to produce encoded symbols from it
    #  encoder.set_const_symbols(data_in)  # this is not support by my current compiled version of kodo
    encoder.set_symbols(data_in)

    # init counter of packets for each node
    counter_encoder = 0
    counter_recoder = 0
    counter_decoder = 0

    # init the number of packets that recoder have recieved
    # before recoder start to send a packet ( 0 : the recoder do not send packets )
    num_before_send = 0

    # if the reciever do not get all the packets
    # the encoder and helper will always send coded packets
    while not decoder.is_complete():
        # Encode a packet into the payload buffer
        # TODO: select either encoder or recoder as packet source
        # the rank of helper play a important role here
        # TODO: count packets sent by encoder and recoder

        # firstly the systematic encoding should be used

        # if the encoder send a packet
        packet = encoder.write_payload()
        counter_encoder += 1

        # if the recoder send a packet
        #  packet = recoder.write_payload()
        #  counter_recoder += 1

        # broadcast the packet from the encoder
        # TODO: simulate losses
        #  recoder.read_payload(packet)

        # simulate losses using random number

        # the link between encoder and decoder
        if np.random.uniform(0, 1) < e_3:
            decoder.read_payload(packet)

        # TODO: count linear dependent packets by packet source
        # TODO: count total packets sent(encoder_num + recoder_num)
        total_packets = counter_encoder + counter_recoder

    # copy the symbols from the decoders

    data_out = decoder.copy_from_symbols()

    # Check we properly decoded the data
    if data_out == data_in:
        print("data decoded correctly...")
        print("the number of packets from encoder is %d" % counter_encoder)
        print("the number of packets from recoder is %d" % counter_recoder)
        print("the total number of packets sent is %d" % total_packets)

        # Output the statistics using CVS file
        # the format is

        file = open("statistics.dat", "w+")
        #  file.write(str(counter_encoder))
        file.close()
    else:
        print("unexpected failure to decode please file a bug report :)")
        sys.exit(1)

if __name__ == "__main__":
    main()
