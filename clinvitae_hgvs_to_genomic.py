#!/usr/bin/env python

import argparse
import pyhgvs as hgvs
import hgvs.utils as hgvs_utils

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


    chrom, offset, ref, alt = hgvs.parse_hgvs_name('NM_000352.3:c.215A>G', genome, get_transcript=get_transcript)
