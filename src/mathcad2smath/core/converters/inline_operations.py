#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def replace_xml(worksheet):
    
    with open(worksheet) as f:
        mathcad_xml = f.read()

    # Provisory inline replace
    with open(worksheet, 'w') as f:
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
