#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Based on learner.js (by Michael Becker and Blake Allen)

import itertools


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
       return __repr__(self)


class Hypothesis(object):

    def __init__(self, changes, associated_forms):
        self.changes = changes
        self.associated_forms = associated_forms

    def __repr__(self):
        # needs aesthetic improvement
        example_count = min(5, len(self.associated_forms))
        return '{0}\n{1}...\n'.format(self.changes, [''.join([s for s in form['base'] if s != None]) for form in self.associated_forms[:example_count]])

    def __str__(self):
       return __repr__(self)





def create_and_distill_hypotheses(alignments):

    unfiltered_hypotheses = []
    for alignment in alignments:
        base = [column['elem1'] for column in alignment]
        derivative = [column['elem2'] for column in alignment]
        basic_changes = find_basic_changes(alignment)
        possibilities_for_all_changes = [create_change_possibilities(c, alignment) for c in basic_changes]
        product = list(itertools.product(*possibilities_for_all_changes))
        for cp in product:
            unfiltered_hypotheses.append(Hypothesis(cp, [{'base':base, 'derivative':derivative}]))

    return unfiltered_hypotheses



def find_basic_changes(alignment):
    """Find the differences between the aligned base and derivative.
    Return differences as Changes with positive indices as positions.
    """
    changes = []
    surface_i = 0
    for column in alignment:
        if column['elem1'] != column['elem2']:
            if column['elem1'] == None:
                changes.append(Change('insert', surface_i*2, column['elem1'], column['elem2']))
                # surface_i does not increment
            elif column['elem2'] == None:
                changes.append(Change('delete', surface_i*2+1, column['elem1'], column['elem2']))
                surface_i += 1
            else:
                changes.append(Change('mutate', surface_i*2+1, column['elem1'], column['elem2']))
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

