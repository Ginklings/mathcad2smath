#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def convert_summation(root):
    # Sumation convert
    for summation in root.findall('.//{http://schemas.mathsoft.com/math30}summation/..'):
        lb = summation.find('{http://schemas.mathsoft.com/math30}lambda')
        bound_vars = lb.find('{http://schemas.mathsoft.com/math30}boundVars')
        bound_var = bound_vars.find('{http://schemas.mathsoft.com/math30}id').text
        new_bound_var_xml = '<ml:imag xmlns:ml="http://schemas.mathsoft.com/math30" symbol="{}">1</ml:imag>'.format(bound_var)
        new_bound_var = ET.fromstring(new_bound_var_xml)
        bounds = summation.find('{http://schemas.mathsoft.com/math30}bounds')
        summation_children = [child for child in summation]
        for child in summation_children:
            summation.remove(child)
        summation.append(ET.fromstring('<ml:id xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">sum</ml:id>'))
        for child in lb.findall('.//{http://schemas.mathsoft.com/math30}id/..'):
            to_replace = []
            for ml_id in child:
                if ml_id.text == bound_var:
                    to_replace.append((child, ml_id))
            for parent, ml_id in to_replace:
                ml_id_index = list(parent).index(ml_id)
                parent.remove(ml_id)
                parent.insert(ml_id_index, new_bound_var)
        for child in lb:
            if not child.tag == '{http://schemas.mathsoft.com/math30}boundVars':
                summation.append(child)
        summation.append(new_bound_var)
        for child in bounds:
            summation.append(child)
