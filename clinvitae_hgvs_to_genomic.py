#!/usr/bin/env python

import csv
import argparse
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils

from pygr.seqdb import SequenceFileDB


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input file")
    parser.add_argument('-g', '--genome', help="Genome reference FASTA")
    parser.add_argument('-r', '--refgene', help="RefGene Transcripts")
    parser.add_argument('-o', '--outfile', help="Output file name")

    args = parser.parse_args()

    genome = SequenceFileDB(args.genome)

    with open(args.refgene) as infile:
        transcripts = hgvs_utils.read_transcripts(infile)

    # Provide a callback for fetching a transcript by its name.
    def get_transcript(name):
        return transcripts.get(name)

    with open(args.infile, 'r') as infile:
        with open(args.outfile, 'w') as outfile:
            reader = csv.reader(infile, dialect='tab-excel')
            header = reader.next()
            for row in reader:
                chrom, offset, ref, alt = hgvs.parse_hgvs_name(row[1], genome, get_transcript=get_transcript)
                outfile.write("{}\t{}\t{}\t{}\n".format(chrom, offset, ref, alt))
