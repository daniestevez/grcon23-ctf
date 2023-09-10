#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dvbs2 Iqfile
# GNU Radio version: 3.10.6.0

from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np




class dvbs2_iqfile(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dvbs2 Iqfile", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1000000
        self.taps = taps = 100
        self.samp_rate = samp_rate = symbol_rate * 2
        self.rolloff = rolloff = 0.2

        ##################################################
        # Blocks
        ##################################################

        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                0.7,
                1,
                0.48,
                0.07,
                window.WIN_HAMMING,
                6.76))
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, firdes.root_raised_cosine(0.9, samp_rate, samp_rate/2, rolloff, taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.01,
            frequency_offset=(-2347.587 / samp_rate),
            epsilon=(1 - 1.237e-6),
            taps=[np.exp(1j * 0.817)],
            noise_seed=173,
            block_tags=False)
        self.blocks_file_source_2 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/daniel/contracting/grcon23-ctf/plframes_all.c64', False, 0, 0)
        self.blocks_file_source_2.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/daniel/contracting/grcon23-ctf/dvbs2.sigmf-data', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_interleaved_char_0 = blocks.complex_to_interleaved_char(False, 127)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_interleaved_char_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_2, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_interleaved_char_0, 0))


    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate * 2)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.fft_filter_xxx_0.set_taps(firdes.root_raised_cosine(0.9, self.samp_rate, self.samp_rate/2, self.rolloff, self.taps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.channels_channel_model_0.set_frequency_offset((-2347.587 / self.samp_rate))
        self.fft_filter_xxx_0.set_taps(firdes.root_raised_cosine(0.9, self.samp_rate, self.samp_rate/2, self.rolloff, self.taps))

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.fft_filter_xxx_0.set_taps(firdes.root_raised_cosine(0.9, self.samp_rate, self.samp_rate/2, self.rolloff, self.taps))




def main(top_block_cls=dvbs2_iqfile, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
