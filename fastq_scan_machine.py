#!/usr/bin/env python

import argparse
import glob
import sys
import HTSeq

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help="Output file name", default="fastq_machine_runIDs.txt")
    args = parser.parse_args()

    fastq_files = glob.glob("*_L001_R1_001.fastq.gz")

    with open(args.output, 'w') as output:
        for fastq in fastq_files:
            parts = fastq.split('_L001_R1_001')
            sample = parts[0]
            fastq_file = HTSeq.FastqReader(fastq)
            read = fastq_file.next()
            read_name_parts = read.name.split(':')
            sys.stdout.write("{}\t{}\n".format(sample, read_name_parts[0]))
            output.write("{}\t{}\n".format(sample, read_name_parts[0]))
