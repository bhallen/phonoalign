#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aligner
import hypothesize

import itertools


alr = aligner.Aligner(feature_file='ex_features.txt', sub_penalty=3.0, tolerance=1.0)


with open('ex_pairs.txt', 'U') as test_file:
    pairs = [line.split('\t') for line in test_file.read().rstrip().split('\n') if len(line) > 0]
    
    all_alignments=[]
    for pair in pairs:
        # print(pair)
        alignments = alr.align(*[form.split(' ') for form in pair])
        # print(alignments)
        for alignment in alignments:
            # alr.display_alignment(alignment)
            all_alignments.append(alignment)
            # print(hypothesize.find_basic_changes(alignment))
            # print(hypothesize.group_changes(hypothesize.find_basic_changes(alignment)))
        #     alr.display_alignment(alignment)
        #     basic_changes = hypothesize.find_basic_changes(alignment)
        #     possibilities_for_all_changes = [hypothesize.create_change_possibilities(c, alignment) for c in basic_changes]
        #     product = itertools.product(*possibilities_for_all_changes)
        #     print(list(product))
        #     print('')
        # print('')

    res = hypothesize.create_and_distill_hypotheses(all_alignments)
    print(res)
