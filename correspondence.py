from collections import defaultdict


def count_correspondences(alignments):
    def elem_sort(elem):
        if elem == None:
            return '(None)'
        else:
            return elem

    corr_dict = defaultdict(int)
    for a in alignments:
        for col in a:
            corr = tuple(sorted([col['elem1'], col['elem2']], key=elem_sort))
            corr_dict[corr] += 1

    return corr_dict