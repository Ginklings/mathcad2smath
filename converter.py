#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lxml import etree
import xml.etree.ElementTree as ET
import os


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


SCHEMA = '{{http://schemas.mathsoft.com/worksheet30}}{}'


def xtag(t):
    return SCHEMA.format(t)


def xpathtag():
    return 


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

    
def converter(planilha):
    if '(SMATH)' in planilha:
        return
    tree = ET.parse(planilha)
    root = tree.getroot()
    ET.register_namespace('', 'http://schemas.mathsoft.com/worksheet30')
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    # ET.register_namespace('ws', 'http://schemas.mathsoft.com/worksheet30')
    ET.register_namespace('ml', 'http://schemas.mathsoft.com/math30')
    ET.register_namespace('u', 'http://schemas.mathsoft.com/units10')
    ET.register_namespace('pv', 'http://schemas.mathsoft.com/provenance10')
    
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
                        pass

            try:
                name = eval.find('{http://schemas.mathsoft.com/math30}id').text
                eval_dict[name] = region
            except:
                try:
                    provenance = eval.find('{http://schemas.mathsoft.com/math30}provenance')
                    name = provenance.find('{http://schemas.mathsoft.com/math30}id').text
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

    out = os.path.join(os.path.dirname(planilha), '(SMATH)' + os.path.basename(planilha))
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
        for tag in ['originRef', 'hash', 'parentRef', 'originComment', 'comment', 'contentHash']:
            mathcad_xml = mathcad_xml.replace(f'pv:{tag}', tag)
        f.write(mathcad_xml)


if __name__ == '__main__':
    from glob import glob
    basedir = r''
    for planilha in glob(os.path.join(basedir, '*.xmcd')):
        print(planilha)
        converter(planilha)
