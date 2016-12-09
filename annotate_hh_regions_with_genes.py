#!/usr/bin/env python

import argparse
import argcomplete
import pybedtools


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input regions in BED format")
    parser.add_argument('-o', '--outfile', help="Output file name")
    parser.add_argument('-a', '--annotations', help="BED format file of genes")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    transcripts = pybedtools.BedTool(args.annotations)
    regions = pybedtools.BedTool(args.infile)

    transcripts_in_regions = transcripts.intersect(regions, u=True)
    transcripts_in_regions.moveto(args.outfile)
