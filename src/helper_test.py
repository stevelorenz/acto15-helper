#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# ###################################################################################
# About  : Project of course actual topics 2015
#          Simulate a topology where an encoder broadcasts packets to the decoder
#          and a helper node
# Author : Xiang,Zuo
# Email  : xianglinks@gmail.com
# Date   : 2015-12-29 18:21:13
# ###################################################################################

import kodo
import sys

import numpy as np


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


def simulate(symbols, symbol_size, e_1, e_2, e_3, tr, data_in, num_sim, results_file):

    # firstly use a Full RLNC coder with GF(2) Field
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    # init lists for statistical results
    encoder_sent_list = []
    recoder_sent_list = []
    total_sent_list = []

    for i in range(num_sim):
        # start test loop ----------------------------------------------------------------

        # creat coder at each node
        # TODO: wether kodo has clean_buffer function of coder
        encoder = encoder_factory.build()
        recoder = decoder_factory.build()
        decoder = decoder_factory.build()

        # put the data buffer to the encoder so that we may start to produce encoded symbols from it
        encoder.set_const_symbols(data_in)

        # init counters for each node
        ct_encoder_sent = 0  # packets sent from encoder
        ct_recoder_sent = 0  # packets sent from recoder
        ct_recoder_recv = 0  # packets recieved by recoder
        ct_decoder_recv = 0  # packets recieved by decoder
        ct_dependent_encoder = 0  # linear dependent packets by packet source

        # flag for alternatively sending by encoder and recoder
        flag = 0  # start from recoder

        # main loop: until the decoder has decoded all the orginal packets
        # systematic coding should be firstly tested
        while not decoder.is_complete():
            # start recieve loop --------------------------------------------------------
            # select either encoder or recoder as packet source
            # determined by the number of packets recieved by recoder

            # only encoder send packets, the recoder keep gathering packets
            if ct_recoder_recv < tr:
                # the encoder send a packet
                packet = encoder.write_payload()
                ct_encoder_sent += 1

                # broadcast the packet from the encoder
                # both recoder and decoder try to recieve the packet
                if np.random.uniform(0, 1) > e_1:
                    # the recoder get the packet
                    recoder.read_payload(packet)
                    ct_recoder_recv += 1

                if np.random.uniform(0, 1) > e_3:
                    # the decoder get the packet
                    r = decoder.rank()  # the number of already decoded packets
                    decoder.read_payload(packet)
                    ct_decoder_recv += 1
                    if r == decoder.rank():
                        ct_dependent_encoder += 1

            # the helper start to send packets(if ct_recoder_recv >= threshold_recoder)
            # test-scenario1: the encoder and recoder send packets alternatively(TDMA)
            else:
                if flag == 0:
                    # recoder send a packet
                    packet = recoder.write_payload()
                    ct_recoder_sent += 1

                    # only the decoder try to get the packet
                    if np.random.uniform(0, 1) > e_2:
                        decoder.read_payload(packet)
                        ct_decoder_recv += 1

                    flag = not flag  # change flag for next round

                else:
                    # encoder sent a packet
                    packet = encoder.write_payload()
                    ct_encoder_sent += 1

                    # broadcast the packet from the encoder
                    # both recoder and decoder try to recieve the packet

                    if np.random.uniform(0, 1) > e_1:
                        # the recoder get the packet
                        recoder.read_payload(packet)
                        ct_recoder_recv += 1

                    if np.random.uniform(0, 1) > e_3:
                        # the decoder get the packet
                        r = decoder.rank()  # the number of already decoded packets
                        decoder.read_payload(packet)
                        ct_decoder_recv += 1
                        if r == decoder.rank():
                            ct_dependent_encoder += 1
                            ct_decoder_recv += 1

                    flag = not flag  # change flag for next round
        # end recieve loop --------------------------------------------------------------

        total_packets_sent = ct_encoder_sent + ct_recoder_sent

        # copy the symbols from the decoders
        data_out = decoder.copy_from_symbols()

        # check we properly decoded the data
        if data_out == data_in:
            # put the results in lists
            encoder_sent_list.append(ct_encoder_sent)
            recoder_sent_list.append(ct_recoder_sent)
            total_sent_list.append(total_packets_sent)

        else:
            print("unexpected failure to decode please file a bug report :)")
            sys.exit(1)
    # end test loop ---------------------------------------------------------------------

    # caculate statistical results

    # for total(encoder plus recoder)
    avg_total_sent = np.average(total_sent_list)
    std_total_sent = np.std(total_sent_list)
    emp_std_total_sent = np.sqrt(float(num_sim) / (num_sim - 1)) * std_total_sent  # get empirical std

    # for encoder
    #  avg_encoder_sent = np.average(encoder_sent_list)
    #  std_encoder_sent = np.std(encoder_sent_list)
    #  emp_std_encoder_sent = np.sqrt(float(num_sim) / (num_sim - 1)) * std_encoder_sent  # get empirical std

    # for recoder
    avg_recoder_sent = np.average(recoder_sent_list)
    std_recoder_sent = np.std(recoder_sent_list)
    emp_std_recoder_sent = np.sqrt(float(num_sim) / (num_sim - 1)) * std_recoder_sent  # get empirical std

    # save the results in a CVS file (path ../test-results)
    data_file = open(results_file, 'a')
    data_str = str(avg_total_sent) + ',' + str(emp_std_total_sent) + ' '
    data_str += str(avg_recoder_sent) + ',' + str(emp_std_recoder_sent) + '\n'
    data_file.write(data_str)
    data_file.close()
