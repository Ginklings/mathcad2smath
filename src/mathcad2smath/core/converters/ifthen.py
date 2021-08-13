#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from mathcad2smath.core.utils import get_index, get_all_children

__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def create_if_apply(ifthen, parent):
    "Create new 'apply' tag element for IF statement"
    new_apply = ET.fromstring('<ml:apply xmlns:ml="http://schemas.mathsoft.com/math30"></ml:apply>')
    new_apply.append(ET.fromstring('<ml:id xmlns:ml=\
        "http://schemas.mathsoft.com/math30" xml:space="preserve">if</ml:id>'))
    new_apply.extend(get_all_children(ifthen))
    if parent:
        parent.append(new_apply)
    return new_apply


def get_current_prog(define, curr_index):
    return list(define.findall('.//{http://schemas.mathsoft.com/math30}program/..'))[curr_index]


def convert_ifthen(root):
    "Convert the ifThen/Otherwise to if/else"
    for define in root.findall('.//{http://schemas.mathsoft.com/math30}define'):
        prog_parents = define.findall('.//{http://schemas.mathsoft.com/math30}program/..')
        has_prog_parent = bool(prog_parents)
        curr_index = 0
        while has_prog_parent:
            try:
                prog_parent = get_current_prog(define, curr_index)
            except IndexError:
                break
            for prog in prog_parent:
                if prog.tag == '{http://schemas.mathsoft.com/math30}program':
                    ifthens = prog.findall('{http://schemas.mathsoft.com/math30}ifThen')
                    otherwise = prog.find('{http://schemas.mathsoft.com/math30}otherwise')
                    if len(ifthens) > 0:
                        prog_index = get_index(prog_parent, prog)
                        prog_parent.remove(prog)
                        first_new_apply = None
                        new_apply_parent = None
                        for ifthen in ifthens:
                            last_new_apply = create_if_apply(ifthen, new_apply_parent)
                            new_apply_parent = last_new_apply
                            if not first_new_apply:
                                first_new_apply = last_new_apply
                        if otherwise:
                            last_new_apply.extend(get_all_children(otherwise))
                        else:
                            # Mathcad ifThen may do not have the otherwise
                            # Smath always has a ELSE statement
                            fake_else = ET.fromstring('<ml:real xmlns:ml=\
                                "http://schemas.mathsoft.com/math30">0</ml:real>')
                            last_new_apply.append(fake_else)
                        prog_parent.insert(prog_index, first_new_apply)
                    else:
                        curr_index += 1
