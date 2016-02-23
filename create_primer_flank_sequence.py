#!/usr/bin/env python

import argparse
import pybedtools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bed', help="BED file of target regions")
    parser.add_argument('-r', '--reference', help="Reference FASTA file")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    targets = pybedtools.BedTool(args.bed)
    with open(args.output, 'w') as output:
        for target in targets:
            flank1_start = target.start - 11
            flank1_end = target.start

            flank2_start = target.end
            flank2_end = target.end + 11

            flank1 = pybedtools.BedTool("{} {} {}".format(target.chrom, flank1_start, flank1_end), from_string=True)
            flank2 = pybedtools.BedTool("{} {} {}".format(target.chrom, flank2_start, flank2_end), from_string=True)

            flank1_seq = flank1.sequence(fi=args.reference)
            flank2_seq = flank1.sequence(fi=args.reference)

            target_size = target.end - target.start

            output.write("{name}\t{size}\t{chr}:{start}-{end}\t({flank1}.*{flank2})\n".format(name=target.name,
                                                                                              size=target_size,
                                                                                              chr=target.chrom,
                                                                                              start=target.start,
                                                                                              end=target.end,
                                                                                              flank1=flank1_seq.seqfn.read(),
                                                                                              flank2=flank2_seq.seqfn.read()))
