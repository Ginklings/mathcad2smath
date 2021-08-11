#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lxml import etree
import xml.etree.ElementTree as ET
import os
from glob import glob
from subprocess import PIPE, run as run_command
from mathcad2smath import custom_mathcad_function

__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


SCHEMA = '{{http://schemas.mathsoft.com/worksheet30}}{}'
INCLUDE_TEMPLATE = '''
      <math optimize="false" disable-calc="false">
        <ml:define xmlns:ml="http://schemas.mathsoft.com/math30">
          <ml:id xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">custom_mathcad_functions</ml:id>
          <ml:apply xmlns:ml="http://schemas.mathsoft.com/math30">
            <ml:id xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">include</ml:id>
            <ml:str xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">{}</ml:str>
          </ml:apply>
        </ml:define>
      </math>
      '''

REGION_TEMPLATE = '<region region-id="{}" left="267.75" top="{}" width="271.75" height="18.75" align-x="264.5" align-y="11" show-border="false" show-highlight="false" is-protected="true" z-order="0" background-color="inherit" tag="">{}</region>'

class ConverterSetup(object):
    
    def __init__(self, **kwargs) -> None:
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))


def save_as_sm(xmcd: str, smath_path: str, test=False) -> None:
    smath = os.path.join(smath_path, 'SMathStudio_Desktop.exe')
    command = [smath, '-silent', '-e', '.sm', xmcd]
    save = True
    if test:
        status = run_command(command + ['-t'], stdout=PIPE)
        if 'Testing failed' in status.stdout.decode('utf-8'):
            save = False
            print('Failed to create SM file. Only XMCD file generated.')
    if save:
        run_command(command, stdout=PIPE)


def xtag(t):
    return SCHEMA.format(t)


def add_tag(tags, new):
    if not new.tag in tags:
        tags.append(new.tag)


def create_if_apply(ifthen, parent):
    new_apply = ET.fromstring('<ml:apply xmlns:ml="http://schemas.mathsoft.com/math30"></ml:apply>')
    new_apply.append(ET.fromstring('<ml:id xmlns:ml="http://schemas.mathsoft.com/math30" xml:space="preserve">if</ml:id>'))
    new_apply.extend([child for child in ifthen])
    if parent:
        parent.append(new_apply)
    return new_apply


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


def converter(planilha, setup):
    output_filename = apply_output_pattern(os.path.basename(planilha),
                                           setup.prefix, setup.sufix)
    dirname = os.path.dirname(planilha)
    out = os.path.join(dirname, output_filename)
    print('Output file: ', out)
    
    if not setup.overwrite:
        if os.path.isfile(out):
            print('Skipping: output file exist.')
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
        custom_mathcad_function.save_sm_file(os.path.dirname(planilha))
        include_file('custom\\002E\\sm', parent=regions, region_id=region_id, y_pos=y_pos)
        
    for external_file in setup.add_external:
        y_pos += 15
        region_id += 1
        external = os.path.join(setup.external_path, external_file)
        if os.path.isfile(external):
            include_file(external, parent=regions, region_id=region_id, y_pos=y_pos)
        elif os.path.isfile(external_file):
            include_file(external, parent=regions, region_id=region_id, y_pos=y_pos)
        else:
            for extract_external in glob(external):
                include_file(extract_external, parent=regions, region_id=region_id, y_pos=y_pos)
                y_pos += 15
                region_id += 1

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
    
    # Change function that receive matrix in Smath
    seq_to_matrix_func = ['max', 'min']
    for apply in root.findall('.//{http://schemas.mathsoft.com/math30}apply'):
        ml_id = apply.find('{http://schemas.mathsoft.com/math30}id')
        if ml_id is not None:
            if ml_id.text in seq_to_matrix_func:
                seq = apply.find('{http://schemas.mathsoft.com/math30}sequence')
                if seq is not None:
                    seq_index = list(apply).index(seq)
                    seq_children = [child for child in seq]
                    m_indice = len(seq_children)
                    new_matrix = ET.fromstring('<ml:matrix xmlns:ml="http://schemas.mathsoft.com/math30" rows="1" cols="{}"></ml:matrix>'.format(m_indice))
                    new_matrix.extend(seq_children)
                    apply.remove(seq)
                    apply.insert(seq_index, new_matrix)
    
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
            
    # Add linked external files
    for region in root.findall('.//{http://schemas.mathsoft.com/worksheet30}region'):
        link = region.find('.//{http://schemas.mathsoft.com/worksheet30}link')
        if link is not None:
            delete_all_children(region)
            href_text = link.get('href')
            href = href_text.replace('./', '')
            href_filename = apply_output_pattern(href, setup.prefix, setup.sufix, use_sm_ext=True)
            href_filename_xmcd = apply_output_pattern(href, setup.prefix, setup.sufix)
            if setup.filename:
                href_dirname = os.path.split(href)[0]
                if not href_dirname:
                    href_dirname = dirname
                if not os.path.isfile(os.path.join(href_dirname, href_filename)):
                    if os.path.isfile(os.path.join(href_dirname, href_filename_xmcd)):
                        save_as_sm(os.path.join(href_dirname, href_filename_xmcd), setup.smath_path)
                        if not os.path.isfile(os.path.join(href_dirname, href_filename)):
                            href_filename = href
                    else:
                        href_filename = href
            include_file(href_filename, region=region)        

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
        

    print(out)
    tree.write(out)
    with open(out) as f:
        mathcad_xml = f.read()
        
    # Provisory inline replace
    with open(out, 'w') as f:
        mathcad_xml = mathcad_xml.replace('ml:result', 'result')
        mathcad_xml = mathcad_xml.replace(' /', '/')
        mathcad_xml = mathcad_xml.replace('<ml:indexer/>', '<ml:id xml:space="preserve">el</ml:id>')
        mathcad_xml = mathcad_xml.replace('<ml:vectorSum/>', '<ml:id xml:space="preserve">sum</ml:id>')
        mathcad_xml = mathcad_xml.replace('<ml:matcol/>', '<ml:id xml:space="preserve">col</ml:id>')
        mathcad_xml = mathcad_xml.replace('<ml:localDefine>', '<ml:id xml:space="preserve">line</ml:id><ml:define>')
        mathcad_xml = mathcad_xml.replace('</ml:localDefine>', '</ml:define>')
        mathcad_xml = mathcad_xml.replace('<ml:return>', '')
        line_end_mark = '<ml:real>2</ml:real><ml:real>1</ml:real>'
        mathcad_xml = mathcad_xml.replace('</ml:return>', line_end_mark)
        mathcad_xml = mathcad_xml.replace('<ml:program>', '<ml:apply>')
        mathcad_xml = mathcad_xml.replace('</ml:program>', '</ml:apply>')
        for tag in ['originRef', 'hash', 'parentRef', 'originComment', 'comment', 'contentHash']:
            mathcad_xml = mathcad_xml.replace(f'pv:{tag}', tag)
        f.write(mathcad_xml)
    
    if setup.save_as_sm:
        save_as_sm(out, setup.smath_path, test=True)


def convert_xmcd_in_path(path, setup):
    for worksheet in glob(os.path.join(path, '*.xmcd')):
        print(worksheet)
        try:
            converter(worksheet, setup)
        except:
            print('Error converting file')
        
        
def run(setup):
    print(setup.filename)
    if setup.filename:
        converter(setup.filename, setup)
    elif setup.recursive:
        for path_content in os.walk(setup.basedir):
            convert_xmcd_in_path(path_content[0], setup)
    else:
        convert_xmcd_in_path(setup.basedir, setup)
