import h5py
import argparse
import argcomplete
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="HH Output file")
    parser.add_argument('-o', '--outfile', help="Output file name")
    parser.add_argument('-a', '--annotations', help="SNP annotations file for HH")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    f = h5py.File(args.infile, "r")
