#!/usr/bin/env python3

import argparse
import os.path as osp
import time
from textwrap import dedent

import h5py as h5
import numpy as np


inp_list_file = "indexed_p700000_r0030.lst"
inp_file = "../../data/p700000_r0030_proc.cxi"
out_file = "indexed_p700000_r0030_vds.h5"


def prep_h5data(n_frames: int):
    start_time = time.time()
    print("Start writing the data...")

    self_dir = osp.split(osp.realpath(__file__))[0]
    inp_list_path = osp.join(self_dir, inp_list_file)
    inp_file_path = osp.join(self_dir, inp_file)
    out_file_path = osp.join(self_dir, out_file)

    indexed_frames = []
    with open(inp_list_path, 'r') as flst:
        for line in flst:
            file_name, frame_num_str = line.split(' //')
            frame_num = int(frame_num_str)
            indexed_frames.append((file_name, frame_num))

    if n_frames > 0:
        n_frames_store = min(n_frames, len(indexed_frames))
    else:
        n_frames_store = len(indexed_frames)

    out_orig_id = []
    out_data = []
    out_mask = []
    out_trainId = []
    out_pulseId = []
    with h5.File(inp_file_path, 'r') as h5in:
        for indexed_frame in indexed_frames[:n_frames_store]:
            fr_id = indexed_frame[1]
            out_orig_id.append(fr_id)
            out_data.append(h5in['/entry_1/data_1/data'][fr_id])
            out_mask.append(h5in['/entry_1/data_1/mask'][fr_id])
            out_trainId.append(h5in['/entry_1/trainId'][fr_id])
            out_pulseId.append(h5in['/entry_1/pulseId'][fr_id])

    store_orig_id = np.array(out_orig_id)
    store_data = np.array(out_data)
    store_mask = np.array(out_mask)
    store_trainId = np.array(out_trainId)
    store_pulseId = np.array(out_pulseId)

    with h5.File(out_file_path, 'w') as h5f:
        h5f.create_dataset(
            '/entry_1/originalId', data=store_orig_id, dtype='int32')
        h5f.create_dataset(
            '/entry_1/instrument_1/detector_1/data', data=store_data, dtype='float32')
        h5f.create_dataset(
            '/entry_1/instrument_1/detector_1/mask', data=store_mask, dtype='int32')
        h5f.create_dataset(
            '/entry_1/trainId', data=store_trainId, dtype='int64')
        h5f.create_dataset(
            '/entry_1/pulseId', data=store_pulseId, dtype='int64')
        h5f['/entry_1/data_1'] = h5.SoftLink('/entry_1/instrument_1/detector_1')

    proc_time = time.time() - start_time
    print(f"Finished in {proc_time:4.2f} s.")


def main(argv=None):
    example = dedent("""
        Example:

            ./prep_h5data.py 100
    """)
    ap = argparse.ArgumentParser(
        'prep_h5data.py', epilog=example,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Write an HDF5 file with selected data frames.'
    )
    ap.add_argument(
        'n_frames',
        help="Number of frames to be stored."
    )
    args = ap.parse_args(argv)
    n_frames = int(args.n_frames)

    prep_h5data(n_frames)


if __name__ == "__main__":
    main()
