#!/usr/bin/env python\
import sys
import csv
import argparse
import argcomplete
from toil.job import Job
from ddb_ngsflow import pipeline


def convert2pe(job, row):
    bamfile = row[0]
    elements = bamfile.split('.')
    lane_id = elements[2]
    sample_id = elements[4]

    outfile1 = "{}.{}.R1.fastq".format(sample_id, lane_id)
    outfile2 = "{}.{}.R2.fastq".format(sample_id, lane_id)

    logfile = "convert_{}.log".format(bamfile)

    command = ("bedtools bamtofastq",
               "-i {}".format(bamfile),
               "-fq {}".format(outfile1),
               "-fq2 {}".format(outfile2))

    job.fileStore.logToMaster("Running command {} and logging to {}\n".format(command, logfile))
    pipeline.run_and_log_command(command, logfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file with list of file names to convert')

    Job.Runner.addToilOptions(parser)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    root_job = Job.wrapJobFn(pipeline.spawn_batch_jobs, cores=1)

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        for row in reader:
            job = Job.wrapJobFn(convert2pe, row, cores=1)
            root_job.addChild(job)

    Job.Runner.startToil(root_job, args)
