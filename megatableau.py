#!/usr/bin/python
# -*- coding: utf-8 -*-

#### ####
#### Based on rdaland/PhoMEnt.git, commit 74f5c43997185aef2d29a7c7dfdac3b5acd760df, from May 2014 ####
#### ####

import sys
from collections import defaultdict
import numpy
import math
import re

class MegaTableau(object):

    """
    A representation of tableaux for manipulation by the maxent learner.
    Derived from a file of tab-delimited tableaux.
    Contains the following attributes:
        self.constraints -------- list of constraint names
            this is found on the first line of the input file
        self.weights ------------ a list of weights for constraints
        self.tableau ------------ a dictionary of dictionaries:
            {input: {output: [freq, violDic, maxentScore]}}
            freq = float()
            violDic = dictionary of constraint violations (integers). 
                Keys are constraint indices, based on order of constraints in self.constraints
            maxentScore = e**harmony. Initialized to zero (because harmony is undefined without weights).
    Contains the following methods:
        self.read_megt_file(megt_file) - moves the data from the .txt file to the attributes
            self.weights is not populated.
        self.read_weights_file(megt_file) - populates self.weights
    """
    
    def __init__(self, sublexicon, constraints):
        """
        sublexicon -- a sublexicon (originally a hypothesis) from hypothesize.py
        constraints -- a list of strings corresponding to the phonological constraints to be weighted
        """
        self.constraints = self.create_re_constraints(constraints)
        self.constraint_names = constraints
        self.weights = numpy.zeros(len(self.constraints))
        self.gaussian_priors = {}
        self.tableau = defaultdict(dict)
        self.populate_tableau(sublexicon)


    def create_re_constraints(self, constraints):
        """To-do: add the ability to translate featural constraints
        """
        return [re.compile(c) for c in constraints]


    def populate_tableau(self, sublexicon):
        outputs = {}
        for af in sublexicon.associated_forms:
            violations = {}
            for c in range(len(self.constraints)):
                these_violations = len(self.constraints[c].findall(af['base']))
                if these_violations > 0:
                    violations[c] = these_violations
            outputs[af['base']] = [af['probability'], violations, 0]
        self.tableau = {'': outputs}