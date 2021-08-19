#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lxml import etree
import xml.etree.ElementTree as ET
import os
from glob import glob

from mathcad2smath import custom_mathcad_functions
from mathcad2smath.core.converters.ifthen import convert_ifthen
from mathcad2smath.core.converters.sequence_to_matrix import function_var_to_matrix
from mathcad2smath.core.converters.summation import convert_summation
from mathcad2smath.core.converters.link import convert_link

from mathcad2smath.core.converters import inline_operations
from mathcad2smath.core.utils import save_as_sm, apply_output_pattern, include_file, log

__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


SCHEMA = '{{http://schemas.mathsoft.com/worksheet30}}{}'

class ConverterSetup(object):
    
    def __init__(self, **kwargs) -> None:
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))


def converter(planilha, setup):
    output_filename = apply_output_pattern(os.path.basename(planilha),
                                           setup.prefix, setup.sufix)
    dirname = os.path.dirname(planilha)
    out = os.path.join(dirname, output_filename)
    log('Output file: ', out)
    
    if not setup.overwrite:
        if os.path.isfile(out):
            log('Skipping: output file exist.')
            return
    
    # Dont convert files with output filename pattern
    file_prefix = ''
    file_sufix = ''
    if setup.prefix:
        nchar_prefix = len(setup.prefix)
        file_prefix = os.path.basename(planilha)[:nchar_prefix]
    if setup.sufix:
        nchar_sufix = len(setup.sufix)
        file_sufix = os.path.basename(planilha)[-nchar_sufix:]
    if setup.prefix == file_prefix and setup.sufix == file_sufix:
        log('Dont convert files with output filename pattern')
        return

    tree = ET.parse(planilha)
    root = tree.getroot()
    ET.register_namespace('', 'http://schemas.mathsoft.com/worksheet30')
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    # ET.register_namespace('ws', 'http://schemas.mathsoft.com/worksheet30')
    ET.register_namespace('ml', 'http://schemas.mathsoft.com/math30')
    ET.register_namespace('u', 'http://schemas.mathsoft.com/units10')
    ET.register_namespace('pv', 'http://schemas.mathsoft.com/provenance10')
    
    regions = root.find('{http://schemas.mathsoft.com/worksheet30}regions')
    
    y_pos = 0
    region_id = 999909
    if not setup.ignore_custom:
        log('Creating custom.sm file...')
        custom_mathcad_functions.save_sm_file(os.path.dirname(planilha))
        include_file('custom\\002E\\sm', parent=regions, region_id=region_id, y_pos=y_pos)
        
    for external_file in setup.add_external:
        log("Adding user's external files...")
        y_pos += 15
        region_id += 1
        external = os.path.join(setup.external_path, external_file)
        if os.path.isfile(external):
            log('File: ', external, ident='  ')
            include_file(external, parent=regions, region_id=region_id, y_pos=y_pos)
        elif os.path.isfile(external_file):
            log('File: ', external_file, ident='  ')
            include_file(external, parent=regions, region_id=region_id, y_pos=y_pos)
        else:
            for extract_external in glob(external):
                log('File: ', extract_external, ident='  ')
                include_file(extract_external, parent=regions, region_id=region_id, y_pos=y_pos)
                y_pos += 15
                region_id += 1

    log('Converting ifThen/Otherwise statement...')
    convert_ifthen(root)
    
    log('Converting function inputs to matrix...')
    function_var_to_matrix(root)
    
    log('Change evaluate value position if before assign...')
    # Change result's position if the result is before assign
    define_dict = {}
    eval_dict = {}
    for region in root.findall('.//{http://schemas.mathsoft.com/worksheet30}region'):
        math = region.find('{http://schemas.mathsoft.com/worksheet30}math')
        if math is not None:
            define = math.find('{http://schemas.mathsoft.com/math30}define')
            eval = math.find('{http://schemas.mathsoft.com/math30}eval')
            try:
                name = define.find('.//{http://schemas.mathsoft.com/math30}id').text
                define_dict[name] = region
            except:
                try:
                    provenance = math.find('{http://schemas.mathsoft.com/math30}provenance')
                    define = provenance.find('{http://schemas.mathsoft.com/math30}define')
                    name = define.find('{http://schemas.mathsoft.com/math30}id').text
                    define_dict[name] = region
                except:
                    try:
                        apply = math.find('{http://schemas.mathsoft.com/math30}apply')
                        define = apply.find('{http://schemas.mathsoft.com/math30}define')
                        name = define.find('{http://schemas.mathsoft.com/math30}id').text
                        define_dict[name] = region
                    except:
                        try:
                            define = math.find('{http://schemas.mathsoft.com/math30}define')
                            function = define.find('{http://schemas.mathsoft.com/math30}function')
                            name = function.find('{http://schemas.mathsoft.com/math30}id').text
                            define_dict[name] = region
                        except:
                            pass

            try:
                name = eval.find('{http://schemas.mathsoft.com/math30}id').text
                if not name in eval_dict.keys():
                    eval_dict[name] = region
            except:
                try:
                    provenance = eval.find('{http://schemas.mathsoft.com/math30}provenance')
                    name = provenance.find('{http://schemas.mathsoft.com/math30}id').text
                    if not name in eval_dict.keys():
                        eval_dict[name] = region
                except:
                    pass

    for name in eval_dict.keys():
        eval_pos = float(eval_dict[name].get('top'))
        define_pos = float(define_dict[name].get('top'))
        if eval_pos < define_pos:
            eval_dict[name].set('top', str(define_pos))

    log('Converting summation statement...')
    convert_summation(root)
    
    log('Converting external link statement...')
    convert_link(root, dirname, setup)

    # Change function in if statement
    # recursive function dont work in a if condition
    # all_functions = {}
    # for region in root.findall('.//{http://schemas.mathsoft.com/worksheet30}region'):
    #     if has_if(region):
    #         for if_case in get_all_if(region):
    #             for apply in if_case[0].findall('.//{http://schemas.mathsoft.com/math30}apply'):
    #                 if list(apply)[0].text in all_functions.keys():
    #                     list(apply)[0].text = '_if__' + list(apply)[0].text
    #     if is_function(region):
    #         all_functions[get_define_name(region)] = region
    #     else:
    #         if get_define_name(region) in all_functions.keys():
    #             del all_functions[get_define_name(region)]

    log('Writing file...')
    tree.write(out)
    
    log('Operating inline replaces...')
    inline_operations.replace_xml(out)
    log('XMCD file saved.')

    if setup.save_as_sm:
        log('Saving as SM file...')
        save_as_sm(out, setup.smath_path, test=True)


def convert_xmcd_in_path(path, setup):
    for worksheet in glob(os.path.join(path, '*.xmcd')):
        convert_worksheet(worksheet, setup)


def convert_worksheet(worksheet, setup):
    try:
        print('Converting file: ', worksheet)
        converter(worksheet, setup)
    except:
        print('Error converting file')


def run(setup):
    if setup.filename:
        convert_worksheet(setup.filename, setup)
    elif setup.recursive:
        print('Converting all files recursively in ', setup.basedir)
        for path_content in os.walk(setup.basedir):
            print('Current directory: ', path_content[0])
            convert_xmcd_in_path(path_content[0], setup)
    else:
        print('Converting all files in ', setup.basedir)
        convert_xmcd_in_path(setup.basedir, setup)
