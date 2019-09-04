#!/usr/bin/env python

import sys
import argparse

from ddb import configuration
from collections import defaultdict

def get_all_amplicons(job, samples):
    job.fileStore.logToMaster("Building list of all amplicons from samples set\n")
    amplicons_list = list()
    for sample in samples:
        for library in samples[sample]:
            report_panel_path = "/mnt/shared-data/ddb-configs/disease_panels/{}/{}" \
                                "".format(samples[sample][library]['panel'], samples[sample][library]['report'])
            target_amplicons = utils.get_target_amplicons(report_panel_path)
            for amplicon in target_amplicons:
                if amplicon not in amplicons_list:
                    amplicons_list.append(amplicon)

    return amplicons_list


def get_coverage_data_all_amplicons(amplicons_list, addresses, authenticator):
    job.fileStore.logToMaster("Retrieving coverage data for all libraries in database for all amplicons\n")
    connection.setup(addresses, "coveragestore", auth_provider=authenticator)

    amplicon_coverage_stats = defaultdict(dict)

    for amplicon in amplicons_list:
        coverage_values = list()

        coverage_data = AmpliconCoverage.objects.timeout(None).filter(
            AmpliconCoverage.amplicon == amplicon
        )
        ordered_samples = coverage_data.order_by('sample', 'run_id').limit(coverage_data.count() + 1000)
        for result in ordered_samples:
            coverage_values.append(result.mean_coverage)

        amplicon_coverage_stats[amplicon]['median'] = np.median(coverage_values)
        amplicon_coverage_stats[amplicon]['std_dev'] = np.std(coverage_values)
        amplicon_coverage_stats[amplicon]['min'] = np.amin(coverage_values)
        amplicon_coverage_stats[amplicon]['max'] = np.amax(coverage_values)

    return amplicon_coverage_stats


def process_sample(parse_functions, sample, samples, config, amplicon_list):

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples_file',
                        help="Input configuration file for samples")
    parser.add_argument('-c', '--configuration',
                        help="Configuration file for various settings")
    parser.add_argument('-l', '--list',
                        help="List file of SNPs to process")

    args = parser.parse_args()

    sys.stdout.write("Parsing configuration data\n")
    config = configuration.configure_runtime(args.configuration)

    sys.stdout.write("Parsing sample data\n")
    samples = configuration.configure_samples(args.samples_file, config)

    sample_cov_data = defaultdict(lambda: defaultdict())

    for sample in samples:
        sys.stdout.write("Processing sample {}\n".format(sample))
        sample_cov_data[sample] = process_sample(parse_functions, sample,
                                                 samples, config, snps)

    sys.stdout.write("Writing out data\n")
    with open("glioma_snp_data.txt", 'wb') as out:
        out.write("SNP\tChr\tPos")
        for sample in samples:
            out.write("\t{} - AAF\t{} - Depth".format(sample, sample))
        out.write("\n")
        for snp in snps:
            out.write("{}".format(snp))
            for sample in samples:
                if sample_snp_data[sample][snp]:
                    out.write("\t{}\t{}".format(sample_snp_data[sample][snp]['freq'],
                                                sample_snp_data[sample][snp]['depth']))
                else:
                    out.write("\t-\t-")
            out.write("\n")
