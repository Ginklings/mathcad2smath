#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import os
from subprocess import PIPE, run as run_command

from mathcad2smath.core.templates import *


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def log(msg, optional='', ident=''):
    print(ident + MSG_PREFIX.format(msg), optional)


def save_as_sm(xmcd: str, smath_path: str, test=False) -> None:
    smath = os.path.join(smath_path, 'SMathStudio_Desktop.exe')
    command = [smath, '-silent', '-e', '.sm', xmcd, '-w', '6000']
    save = True
    if test:
        status = run_command(command + ['-t'], stdout=PIPE, check=False)
        stdout = status.stdout.decode('utf-8')
        if 'Testing failed' in stdout:
            if len(stdout.split('Testing file')) > 1:
                for line in stdout.split('Testing file')[1].split('\n'):
                    if 'Error: ' in line:
                        if not 'content differs.' in line:
                            save = False
                            log('Failed to create SM file. Only XMCD file generated.')
    if save:
        run_command(command, stdout=PIPE, check=False)


def include_file(filename, parent=None, region=None, region_id=None, y_pos=None):
    to_include = INCLUDE_TEMPLATE.format(filename)
    if region is None:
        region_to_include = REGION_TEMPLATE.format(region_id, y_pos, to_include)
        parent.insert(0, ET.fromstring(region_to_include))
    else:
        region.insert(0, ET.fromstring(to_include))


def get_all_children(root):
    return [child for child in root]


def delete_all_children(root):
    for child in get_all_children(root):
        root.remove(child)


def apply_output_pattern(name, prefix, sufix, ext='.xmcd', use_sm_ext=False):
    output_filename = prefix + name
    ext_pos = -len(ext)
    if use_sm_ext:
        ext = '.sm'
    return output_filename[:ext_pos] + sufix + ext


def has_if(element):
    for el_id in element.findall('.//{http://schemas.mathsoft.com/math30}id'):
        if el_id.text == 'if':
            return True
    return False
    

def get_index(parent, child):
    return list(parent).index(child)


def get_all_if(element):
    all_ifs = []
    if_parents = element.findall('.//{http://schemas.mathsoft.com/math30}id/..')
    for parent in if_parents:
        for el_id in parent.findall('{http://schemas.mathsoft.com/math30}id'):
            if el_id.text == 'if':
                if_index = get_index(parent, el_id)
                condition = list(parent)[if_index + 1]
                then = list(parent)[if_index + 2]
                else_then = list(parent)[if_index + 3]
                all_ifs.append((condition, then, else_then))
    return all_ifs


def is_function(element):
    math = element.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    if math is not None:
        define = math.find('.//{http://schemas.mathsoft.com/math30}define')
        if define is not None:
            if list(define)[0].tag == '{http://schemas.mathsoft.com/math30}function':
                return True
    return False


def get_define_name(element):
    math = element.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    name = ''
    if math is not None:
        define = math.find('.//{http://schemas.mathsoft.com/math30}define')
        if define is not None:
            name = define.find('.//{http://schemas.mathsoft.com/math30}id').text
    return name
