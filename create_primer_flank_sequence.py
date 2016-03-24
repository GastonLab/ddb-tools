#!/usr/bin/env python

import argparse
import pybedtools
from pyfaidx import Fasta

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bed', help="BED file of target regions")
    parser.add_argument('-r', '--reference', help="Reference FASTA file")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    targets = pybedtools.BedTool(args.bed)
    genome = Fasta(args.reference)
    with open(args.output, 'w') as output:
        for target in targets:
            flank1_start = target.start - 11
            flank1_end = target.start

            flank2_start = target.end
            flank2_end = target.end + 11

            flank1_seq = genome[target.chrom][flank1_start:flank1_end].seq
            flank2_seq = genome[target.chrom][flank2_start:flank2_end].seq

            target_size = target.end - target.start

            output.write("{name}\t{size}\t{chr}:{start}-{end}\t({flank1}.*{flank2})\n".format(name=target.name,
                                                                                              size=target_size,
                                                                                              chr=target.chrom,
                                                                                              start=target.start,
                                                                                              end=target.end,
                                                                                              flank1=flank1_seq,
                                                                                              flank2=flank2_seq))
