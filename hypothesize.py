#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Based on aligner.js (by Michael Becker and Blake Allen)


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



def find_changes(alignment):
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