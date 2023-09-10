#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Dvbs2 Encode
# GNU Radio version: 3.10.6.0

from gnuradio import blocks
import pmt
from gnuradio import dtv
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class dvbs2_encode(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dvbs2 Encode", catch_exceptions=True)

        ##################################################
        # Blocks
        ##################################################

        self.dtv_dvbs2_physical_cc_0 = dtv.dvbs2_physical_cc(
            dtv.FECFRAME_NORMAL,
            dtv.C1_2,
            dtv.MOD_QPSK,
            dtv.PILOTS_OFF,
            0)
        self.dtv_dvbs2_modulator_bc_0 = dtv.dvbs2_modulator_bc(
            dtv.FECFRAME_NORMAL,
            dtv.C1_2,
            dtv.MOD_QPSK,
            dtv.INTERPOLATION_OFF)
        self.dtv_dvbs2_interleaver_bb_0 = dtv.dvbs2_interleaver_bb(
            dtv.FECFRAME_NORMAL,
            dtv.C1_2,
            dtv.MOD_QPSK)
        self.dtv_dvb_ldpc_bb_0 = dtv.dvb_ldpc_bb(
            dtv.STANDARD_DVBS2,
            dtv.FECFRAME_NORMAL,
            dtv.C1_2,
            dtv.MOD_OTHER)
        self.dtv_dvb_bch_bb_0 = dtv.dvb_bch_bb(
            dtv.STANDARD_DVBS2,
            dtv.FECFRAME_NORMAL,
            dtv.C1_2
            )
        self.dtv_dvb_bbscrambler_bb_0 = dtv.dvb_bbscrambler_bb(
            dtv.STANDARD_DVBS2,
            dtv.FECFRAME_NORMAL,
            dtv.C1_2
            )
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_char*1, '/home/daniel/contracting/grcon23-ctf/bbframes.u8', False, 0, 0)
        self.blocks_file_source_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/daniel/contracting/grcon23-ctf/qpsk12_plframes.c64', False)
        self.blocks_file_sink_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_1, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.dtv_dvb_bbscrambler_bb_0, 0))
        self.connect((self.dtv_dvb_bbscrambler_bb_0, 0), (self.dtv_dvb_bch_bb_0, 0))
        self.connect((self.dtv_dvb_bch_bb_0, 0), (self.dtv_dvb_ldpc_bb_0, 0))
        self.connect((self.dtv_dvb_ldpc_bb_0, 0), (self.dtv_dvbs2_interleaver_bb_0, 0))
        self.connect((self.dtv_dvbs2_interleaver_bb_0, 0), (self.dtv_dvbs2_modulator_bc_0, 0))
        self.connect((self.dtv_dvbs2_modulator_bc_0, 0), (self.dtv_dvbs2_physical_cc_0, 0))
        self.connect((self.dtv_dvbs2_physical_cc_0, 0), (self.blocks_file_sink_1, 0))





def main(top_block_cls=dvbs2_encode, options=None):
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
