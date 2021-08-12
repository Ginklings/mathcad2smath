#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


FUNCTIONS_TO_CHANGE = ['max', 'min']


def function_var_to_matrix(root):
    # Change function that receive matrix in Smath
    for apply in root.findall('.//{http://schemas.mathsoft.com/math30}apply'):
        ml_id = apply.find('{http://schemas.mathsoft.com/math30}id')
        if ml_id is not None:
            if ml_id.text in FUNCTIONS_TO_CHANGE:
                seq = apply.find('{http://schemas.mathsoft.com/math30}sequence')
                if seq is not None:
                    seq_index = list(apply).index(seq)
                    seq_children = [child for child in seq]
                    m_indice = len(seq_children)
                    new_matrix = ET.fromstring('<ml:matrix xmlns:ml="http://schemas.mathsoft.com/math30" rows="1" cols="{}"></ml:matrix>'.format(m_indice))
                    new_matrix.extend(seq_children)
                    apply.remove(seq)
                    apply.insert(seq_index, new_matrix)
