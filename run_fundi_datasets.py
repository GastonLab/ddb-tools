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

    command = ["{}".format(config['vcfanno']['bin']),
               "-p",
               "{}".format(config['vcfanno']['num_cores']),
               "--lua",
               "{}".format(config['vcfanno']['lua']),
               "{}".format(samples[name]['vcfanno_config']),
               "{}".format(input_vcf),
               ">",
               "{}".format(output_vcf)]

    job.fileStore.logToMaster("VCFAnno Command: {}\n".format(command))
    pipeline.run_and_log_command(" ".join(command), logfile)

    return output_vcf


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input configuration file for datasets")
    parser.add_argument('-c', '--configuration', help="Configuration file for various settings")
    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    args.logLevel = "INFO"

    root_job = Job.wrapJobFn(pipeline.spawn_batch_jobs, cores=1)
    sys.stdout.write("Processing data from file: {}\n".format(args.infile))
    with open(args.infile, 'rU') as csvfile:
        reader = csv.reader(args.infile)
        reader.next()
        for row in reader:
            dataset = row[17]
            sys.stderr.write("Running FunDi on dataset {}\n".format(dataset))
            fundi_job = Job.wrapJobFn(run_fundi, dataset,
                                      cores=22,
                                      memory="100G")
            root_job.addChild(fundi_job)

    # Start workflow execution
    Job.Runner.startToil(root_job, args)
