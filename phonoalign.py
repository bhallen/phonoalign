#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aligner


al = aligner.Aligner(feature_file='ex_features.txt', tolerance=2.0)


with open('english_sS_pairs.txt', 'U') as test_file:
    pairs = [line.split('\t') for line in test_file.read().rstrip().split('\n') if len(line) > 0]
    
    for pair in pairs:
        print(pair)
        alignments = al.align(*[form.split(' ') for form in pair])
        # print(alignments)
        for alignment in alignments:
            print(al.morpho_related(alignment, 's', 'sh'))
        #     al.display_alignment(alignment)
        #     print('')
        # print('')