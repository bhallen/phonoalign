#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import csv

import aligner
import hypothesize


alr = aligner.Aligner(feature_file='default_feature_file.txt', sub_penalty=3.0, tolerance=1.0)

alignments = []

with open('ex2_pairs.txt', 'U') as training_file:
    trainingreader = csv.reader(training_file, delimiter='\t')
    training = [line for line in trainingreader if len(line) > 0]
    training = [line[:2]+[float(line[2])] if len(line) == 3 else line[:2]+[1.0] for line in training]

    for triple in training:
        for alignment in alr.align(triple[0].split(' '), triple[1].split(' ')):
            alignments.append([alignment]+[triple[2]])

    reduced_hypotheses = hypothesize.create_and_reduce_hypotheses(alignments)
    # print(reduced_hypotheses)

    ready_for_grammars = hypothesize.add_zero_probability_forms(reduced_hypotheses)
    for h in ready_for_grammars:
        print(h)
        print(h.associated_forms)


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



