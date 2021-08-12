#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


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
