__author__ = 'dgaston'

import csv
import sys
import subprocess
import argparse
import argcomplete

from multiprocessing import Pool


def check_return_codes(codes):
    for code in codes:
        check_return_code(code)


def check_return_code(code):
    if code:
        sys.stdout.write("One or more processes did not complete successfully. Exiting\n")
        sys.exit()


def execute_multiprocess(instructions):
    code = subsample_bam(instructions[0], instructions[1], instructions[2], instructions[3])

    return code


def subsample_bam(sample, seed, fraction, iteration):
    """Use samtools view to subsample an input file to the specified fraction"""

    logfile = "subsample-{}-{}-{}.log".format(sample, fraction, iteration)
    output = "subsample-{}-{}-{}.bam".format(sample, fraction, iteration)
    command = "samtools view -s {seed}.{fraction} -b {input} > {output}".format(seed=seed, fraction=fraction,
                                                                                input=sample, output=output)

    with open(logfile, "wb") as err:
        sys.stdout.write("Executing {com} and writing to logfile {log}\n".format(com=command, log=logfile))
        err.write("Command: {comm}\n".format(comm=command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=err, shell=True)
        process_return = p.communicate()
        code = p.returncode

        return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input file of sample bam files to use")
    parser.add_argument('-s', '--seed', help="Seed number for reproducible sub-sampling")
    parser.add_argument('-n', '--number', help="Number of iterations per sample to perform", default=1)
    parser.add_argument('-t', '--threads', help="Number of parallel threads to use", default=1)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    samples = list()
    fractions = [50, 25]
    instructions = list()

    with open(args.infile, 'rb') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        reader.next()
        for row in reader:
            samples.append(row[0])

    pool = Pool(processes=int(args.threads))
    for sample in samples:
        for fraction in fractions:
            iteration = 0
            while iteration < int(args.number):
                instructions.append((sample, int(args.seed), fraction, iteration))
                iteration += 1

    result = pool.map_async(execute_multiprocess, instructions)
    codes = result.get()
    pool.close()
    pool.join()
    check_return_codes(codes)
