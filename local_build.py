#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from subprocess import run, PIPE

__author__ = "André Ginklings"
__credits__ = ["André Ginklings"]


def build(args):
    
    build_status, upload_status, install_status = 0, 0, 0
    
    if not args.ignore_build:
        print('***************** Build *****************')
        print()
        build_command = ['python', '-m', 'build']
        build_status = run(build_command)
        print()
    
    if args.upload:
        print('***************** Upload *****************')
        upload_command = ['python', '-m', 'twine', 'upload', 'dist/*']
        msg = '----------> PyPi'
        if args.test:
            msg += ' test repo'
            upload_command.insert(4, '--repository')
            upload_command.insert(5, 'testpypi')
        print(msg)
        print()
        upload_status = run(upload_command)
        print()
    
    if args.install:
        print('***************** Install *****************')
        install_command = ['python', '-m', 'pip', 'install', '--upgrade']
        msg = '----------> '
        if args.local:
            msg += 'Local repo'
            install_command += ['--use-feature=in-tree-build', '.']
        else:
            if args.test:
                msg += 'Test repo '
                install_command += ['--index-url', 'https://test.pypi.org/simple/', '--no-deps']
            msg += 'PyPi'
            install_command.append('mathcad2smath')
        print(msg)
        print()
        install_status = run(install_command)
        print()
        
    return build_status, upload_status, install_status


def main():
    parser = argparse.ArgumentParser(
        description='For local build, upload pypi, pip install'
    )
    parser.add_argument('-l', '--local',
                        action='store_true',
                        help='Install local build, using with --install flag')
    parser.add_argument('-i', '--install',
                        action='store_true',
                        help='Install after build')
    parser.add_argument('-u', '--upload',
                        action='store_true',
                        help='Upload to PyPi')
    parser.add_argument('-t', '--test',
                        action='store_true',
                        help='Use test repo in upload')
    parser.add_argument('--ignore_build',
                        action='store_true',
                        help='Use test repo in upload')
    args = parser.parse_args()
    build(args)


if __name__ == '__main__':
    main()
