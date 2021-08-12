#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def create_if_apply(ifthen, parent):
    new_apply = ET.fromstring('<ml:apply xmlns:ml="http://schemas.mathsoft.com/math30"></ml:apply>')
    new_apply.append(ET.fromstring('<ml:id xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">if</ml:id>'))
    new_apply.extend([child for child in ifthen])
    if parent:
        parent.append(new_apply)
    return new_apply


def convert_ifthen(root):
    # Change IF statement (Mathcad program-IFTHEN/OTHERWISE to Smath IF/ELSE)
    for define in root.findall('.//{http://schemas.mathsoft.com/math30}define'):
        progs = define.findall('.//{http://schemas.mathsoft.com/math30}program')
        progs_parents = define.findall('.//{http://schemas.mathsoft.com/math30}program/..')
        for i, prog in enumerate(progs):
            ifthens = prog.findall('{http://schemas.mathsoft.com/math30}ifThen')
            otherwise = prog.find('{http://schemas.mathsoft.com/math30}otherwise')
            if len(ifthens) > 0:
                prog_index = list(progs_parents[i]).index(prog)
                progs_parents[i].remove(prog)
                first_new_apply = None
                new_apply_parent = None
                for ifthen in ifthens:
                    last_new_apply = create_if_apply(ifthen, new_apply_parent)
                    new_apply_parent = last_new_apply
                    if not first_new_apply:
                        first_new_apply = last_new_apply
                if otherwise:
                    last_new_apply.extend([child for child in otherwise])
                else:
                    # Mathcad ifThen may do not have the otherwise
                    # Smath always has a ELSE statement
                    fake_else = ET.fromstring('<ml:real xmlns:ml="http://schemas.mathsoft.com/math30">0</ml:real>')
                    last_new_apply.append(fake_else)
                progs_parents[i].insert(prog_index, first_new_apply)
