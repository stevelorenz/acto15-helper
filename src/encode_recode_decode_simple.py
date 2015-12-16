#! /usr/bin/env python
# encoding: utf-8

import os
import sys

import kodo


def main():
    """
    This example simulates a topology where an encoder broadcasts packets to
    the decoder and a helper node. The helper node can support the encoder by
    sending additional packets to the decoder.  But in each step of the
    simulation either only encoder or helper can generate a packet.

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
    symbols = 42
    symbol_size = 1400

    # TODO: parameterize error probabilities e_1, e_2, e_3

    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders

    # TODO: (optional) parameterize different encoders/decoders
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
    # amount a single encoder can encode)
    # Just for fun - fill the input data with random data
    data_in = os.urandom(encoder.block_size())

    # Assign the data buffer to the encoder so that we may start
    # to produce encoded symbols from it
    encoder.set_const_symbols(data_in)

    while not decoder.is_complete():
        # Encode a packet into the payload buffer
        # TODO: select either encoder or recoder as packet source
        # TODO: count packets sent by encoder and recoder
        packet = encoder.write_payload()

        # broadcast the packet from the encoder
        # TODO: simulate losses
        recoder.read_payload(packet)
        decoder.read_payload(packet)

        # TODO: count linear dependent packets by packet source
        # TODO: count total packets sent

    # Both decoder1 and decoder2 should now be complete,
    # copy the symbols from the decoders

    data_out = decoder.copy_from_symbols()

    # Check we properly decoded the data
    if data_out == data_in:
        print("Data decoded correctly")
        # TODO: output statistics
    else:
        print("Unexpected failure to decode please file a bug report :)")
        sys.exit(1)

if __name__ == "__main__":
    main()
