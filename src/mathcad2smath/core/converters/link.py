#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import os
from mathcad2smath.core.utils import delete_all_children, apply_output_pattern, save_as_sm, include_file


__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def convert_link(root, dirname, setup):
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
