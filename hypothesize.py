#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Based on learner.js (by Michael Becker and Blake Allen)

import itertools
import collections
from collections import defaultdict


class Change(object):

    def __init__(self, change_type, position, input_material, output_material):
        self.change_type = change_type
        self.position = position
        self.input_material = input_material
        self.output_material = output_material

    def __repr__(self):
        # needs aesthetic improvement
        return '{0} {1} to {2} at {3}'.format(self.change_type, self.input_material, self.output_material, self.position)

    def __str__(self):
       return self.__repr__()


class Hypothesis(object):

    def __init__(self, changes, associated_forms):
        self.changes = changes
        self.associated_forms = associated_forms

    def __repr__(self):
        # needs aesthetic improvement
        example_count = min(5, len(self.associated_forms))
        return str(self.changes)

    def __str__(self):
       return self.__repr__()





def create_and_distill_hypotheses(alignments):

    unfiltered_hypotheses = []
    for alignment in alignments:
        base = [column['elem1'] for column in alignment]
        derivative = [column['elem2'] for column in alignment]
        basic_changes = find_basic_changes(alignment)
        grouped_changes = group_changes(basic_changes)
        possibilities_for_all_changes = [create_change_possibilities(c, alignment) for c in grouped_changes]
        product = list(itertools.product(*possibilities_for_all_changes))
        for cp in product:
            unfiltered_hypotheses.append(Hypothesis(cp, [{'base':base, 'derivative':derivative}]))
    
    combined_hypotheses = combine_identical_hypotheses(unfiltered_hypotheses)
    combined_hypotheses.sort(key=lambda h: len(h.associated_forms))
    combined_hypotheses.reverse()

    distilled_hypotheses = remove_subset_hypotheses(combined_hypotheses)

    return distilled_hypotheses



def find_basic_changes(alignment):
    """Find the differences between the aligned base and derivative.
    Return differences as Changes with positive indices as positions.
    """
    changes = []
    surface_i = 0
    for column in alignment:
        if column['elem1'] != column['elem2']:
            if column['elem1'] == None:
                changes.append(Change('insert', surface_i*2, [column['elem1']], [column['elem2']]))
                # surface_i does not increment
            elif column['elem2'] == None:
                changes.append(Change('delete', surface_i*2+1, [column['elem1']], [column['elem2']]))
                surface_i += 1
            else:
                changes.append(Change('mutate', surface_i*2+1, [column['elem1']], [column['elem2']]))
                surface_i += 1
        else:
            surface_i += 1

    return changes


def create_change_possibilities(change, alignment, side='both'):
    """Given a change with segments as input and output and a positive index as position,
    return a list of changes with different positions/inputs/outputs.
    """
    change_possibilities = []
    if side in ['left', 'both']:
        change_possibilities.append(change)
    if side in ['right', 'both']:
        new_change = Change(change.change_type, -(len(alignment)*2-1-change.position), change.input_material, change.output_material)
        change_possibilities.append(new_change)

    return change_possibilities


def group_changes(changes):
    """Consolidate same-position insertions and deletions into single changes.
    """
    insertions = [c for c in changes if c.change_type == 'insert']
    deletions = [c for c in changes if c.change_type == 'delete']
    mutations = [c for c in changes if c.change_type == 'mutate']
    inserted_locations = [ins.position for ins in insertions]

    grouped_insertions = []
    for i, ins in enumerate(insertions):
        if i > 0:
            if ins.position == insertions[i-1].position:
                grouped_insertions[-1].output_material += ins.output_material
                continue
        grouped_insertions.append(ins)


    grouped_deletions = []
    for i, dlt in enumerate(deletions):
        if i > 0:
            if dlt.position == deletions[i-1].position+2 and dlt.position-1 not in inserted_locations:
                grouped_deletions[-1].input_material += dlt.input_material
                continue
        grouped_deletions.append(dlt)

    return sorted(grouped_insertions + grouped_deletions + mutations, key=lambda x: x.position)


def combine_identical_hypotheses(hypotheses):
    """Combine hypotheses with the same Change objects, yielding hypotheses with associated assoc_forms
    that are the superset of component hypotheses.
    """
    temp_dict = defaultdict(list)
    for h in hypotheses:
        temp_dict[str(h.changes)].append(h)

    grouped_hypotheses = []
    for gh in temp_dict:
        assoc_forms = [h.associated_forms[0] for h in temp_dict[gh]]
        grouped_hypotheses.append(Hypothesis(temp_dict[gh][0].changes, assoc_forms))

    return grouped_hypotheses


def apply_hypothesis(word, hypothesis):
    """Apply the changes in a hypothesis to a (base) word. Base word can be either
    a list of segments (no Nones) or a space-spaced string.
    """

    def apply_change(current_base, current_derivative, change):
        """Use the given set of changes to derive a new form from the base word.
        May be only one intermediate step in the application of multiple
        changes associated with a single hypothesis/sublexicon.
        """
        change_position = make_index_positive(current_base, change.position)

        changed_base = current_base[:]
        changed_derivative = current_derivative[:]

        if change.change_type == 'insert':
            changed_base[change_position] = [None for s in change.output_material]
            changed_derivative[change_position] = change.output_material
        if change.change_type == 'delete':
            for i, s in enumerate(change.input_material):
                changed_derivative[change_position+(i*2)] = None
        if change.change_type == 'mutate':
            for i, s in enumerate(change.output_material):
                changed_derivative[change_position+(i*2)] = s

        return (changed_base, changed_derivative)

    def join_it(iterable, delimiter):
        """Intersperse the delimiter between all elements of the iterable, as well as at the beginning and end.
        """
        yield delimiter
        it = iter(iterable)
        yield next(it)
        for x in it:
            yield delimiter
            yield x
        yield delimiter

    if isinstance(word, str):
        word = word.split(' ')

    current_base = list(join_it(word, None))
    current_derivative = list(join_it(word, None))

    try:
        for c in hypothesis.changes:
            current_base, current_derivative = apply_change(current_base, current_derivative, c)
    except:
        return 'incompatible'

    return linearize_word(current_derivative)


def make_index_positive(word, index):
    """Return positive index based on word.
    """
    if index >= 0:
        return index
    else:
        return len(word) + index


def linearize_word(word):
    """Create a space-spaced string from a list-formatted word (even one with Nones).
    """
    def flatten(l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, str):
                for sub in flatten(el):
                    yield sub
            else:
                yield el
    flat_noneless = [s for s in list(flatten(word)) if s != None]
    return ' '.join(flat_noneless)


def remove_subset_hypotheses(hypotheses):
    """Condenses the list of hypotheses about the entire dataset into the
    minimum number required to account for all base-derivative pairs.
    """
    small_to_large = hypotheses[::-1]
    for i, small in enumerate(small_to_large):
        large_h_derivatives = []
        for j, large in enumerate(hypotheses):
            if small != 'purgeable' and large != 'purgeable' and large != small:
                small_h_derivatives = [linearize_word(w['derivative']) for w in small.associated_forms]
                small_h_bases = [linearize_word(w['base']) for w in small.associated_forms]
                large_h_derivatives += [apply_hypothesis(base, large) for base in small_h_bases]
                if set(small_h_derivatives) <= set(large_h_derivatives):
                    hypotheses[len(hypotheses)-1-i] = 'purgeable'
                    break

    return [h for h in hypotheses if h != 'purgeable']