#!/usr/bin/env python

import sys
from cyvcf2 import VCF

sys.stdout.write("Reading VCF: {}\n".format(sys.argv[1]))
for variant in VCF(sys.argv[1]):
    sv_length = variant.INFO.get('SVLEN')
    if sv_length > 100000:
        sys.stdout.write("{}:{} length: {}\n".format(variant.CHROM,
                                                     variant.POS,
                                                     sv_length))
