#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aligner
import hypothesize
import correspondence

import itertools


alr = aligner.Aligner(feature_file='default_feature_file.txt', sub_penalty=3.0, tolerance=1.0)

all_alignments = []

selected_alignments = []
with open('tagalog_training.txt', 'U') as test_file:
    pairs = [line.split('\t') for line in test_file.read().rstrip().split('\n') if len(line) > 0]
    
    all_alignments = []

    for pair in pairs:
        alignments = alr.align(*[form.split(' ') for form in pair])
        ### Option 1: just use first alignment for each pair
        # selected_alignments.append(alignments[0])

        ### Option 2: create and distill hypotheses, optimize alignments
        for al in alignments:
            all_alignments.append(al)

# Part of Option 2         
reduced_hypotheses = hypothesize.create_and_reduce_hypotheses(all_alignments)
print(reduced_hypotheses)


# # hypothesis contexts -> selected_alignments
# for h in distilled_hypotheses:
#     for bd in h.associated_forms:
#         alignment = []
#         z = zip(bd['base'], bd['derivative'])
#         for base_seg, deriv_seg in z:
#             alignment.append({'elem1':base_seg, 'elem2':deriv_seg})
#         selected_alignments.append(alignment)

# # Finally:
# cd = correspondence.count_correspondences(selected_alignments)
# print(cd)



