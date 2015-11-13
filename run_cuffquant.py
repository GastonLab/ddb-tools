__author__ = 'dgaston'

import csv
import sys
import subprocess
import argparse
import argcomplete
import multiprocessing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="input configuration file with sample and file data. Tab-delimited")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    annotation = "./cuffmerge/merged.gtf"
    mask = "/data/shared/Genomes/Homo_sapiens/Annotations/rRNA.gtf"

    with open(args.infile, 'r') as infile:
        reader = csv.reader(infile, dialect="excel-tab")
        for row in reader:
            sample = row[0].strip()
            directory = "./{}".format(sample)
            bam_file = "./BAMs/{}.merged.bam".format(sample)

            logfile = "{}.cuffquant.log".format(sample)
            command = "cuffquant -p {cores} -o {dir} -M {mask} -u --library-type fr-firststrand " \
                      "{ann} {reads}".format(reads=bam_file, ann=annotation, mask=mask, dir=directory,
                                             cores=multiprocessing.cpu_count())

            sys.stdout.write("Executing cuffquant for sample {sample}\n".format(sample=sample))
            with open(logfile, "wb") as err:
                sys.stdout.write("Executing {com} and writing to logfile {log}\n".format(com=command, log=logfile))
                err.write("Command: {comm}\n".format(comm=command))
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=err, shell=True)
                output = p.communicate()
                code = p.returncode
                if code:
                    raise RuntimeError("An error occurred when executing the commandline: {}. "
                                       "Please check the logfile {} for details\n".format(command, logfile))
