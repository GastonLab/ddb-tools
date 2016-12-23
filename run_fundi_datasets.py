#!/usr/bin/env python

# Standard packages
import csv
import sys
import argparse

# Third-party packages
from toil.job import Job
from ddb_ngsflow import pipeline


def run_fundi(job, root_name):
    """Take the specified VCF and use vcfanno to add additional annotations
       :param config: The configuration dictionary.
       :type config: dict.
       :param sample: sample name.
       :type sample: str.
       :param input_vcf: The input_vcf file name to process.
       :type input_vcf: str.
       :returns:  str -- The output vcf file name.
       """

    logfile = "{}.fundi.log".format(root_name)

    command = ["perl ./FunDi.pl",
               "-a",
               "{}.aa_modified_nodash.phy".format(root_name),
               "-o",
               "{}.aa_modified_nodash_subtree".format(root_name),
               "-m LG+F+G",
               "-s",
               "{}.nh.def".format(root_name),
               "-P iqtree",
               "-r 4",
               "-t",
               "{}.nh.newick".format(root_name),
               "-N 22"]

    mv_fundi_log = "mv FunDi.log {}_FunDi.log".format(root_name)

    job.fileStore.logToMaster("FunDi Command: {}\n".format(command))
    pipeline.run_and_log_command(" ".join(command), logfile)

    job.fileStore.logToMaster("Rename file Command: {}\n".format(command))
    pipeline.run_and_log_command(" ".join(mv_fundi_log), logfile)

    return logfile


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input configuration file for datasets")
    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    args.logLevel = "INFO"

    root_job = Job.wrapJobFn(pipeline.spawn_batch_jobs, cores=1)
    sys.stdout.write("Processing data from file: {}\n".format(args.infile))
    with open(args.infile, 'rU') as csvfile:
        reader = csv.reader(args.infile, dialect='excel-tab')
        reader.next()
        for row in reader:
            print row
            dataset = row[17]
            sys.stderr.write("Setting up FunDi run on dataset {}\n".format(dataset))
            fundi_job = Job.wrapJobFn(run_fundi, dataset,
                                      cores=22,
                                      memory="100G")
            root_job.addChild(fundi_job)

    # Start workflow execution
    sys.stdout.write("Executing analyses\n")
    Job.Runner.startToil(root_job, args)
