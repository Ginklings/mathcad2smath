"""This module convert XMCD mathcad files in XMCD compatible with Smath Studio"""

import argparse
from mathcad2smath.converter import run
from mathcad2smath.app.app import run_app

def mathcad2smath(args):
    """Execute the command line"""
    if args.gui:
        run_app()
    else:
        if args.overwrite:
            print('outputs files will be overwriten')
        if not args.filename:
            if args.recursive:
                print('The search will be recursive')
        else:
            print('Converting file: ', args.filename)
        print('The basedir directory is: ', args.basedir)
        print('The output prefix: ', args.prefix)
        print('The output sufix: ', args.sufix)
        if args.ignore_custom:
            print('Skipping create custom.sm file...')
        else:
            print('The custom.sm file will be created...')
        for external in args.add_external:
            print('Adding file: {} from {}'.format(external, args.external_path))
        run(setup=args)



def main():
    """Main command line routine"""
    parser = argparse.ArgumentParser(
        description='Convert XMCD mathcad files into XMCD compatible with Smath Studio'
    )
    parser.add_argument('-o', '--overwrite',
                        action='store_true',
                        help='Overwrite the output file if exist')
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help='Find XMCD files recursively')
    parser.add_argument('-d', '--basedir',
                        default='.',
                        help="The basedir to convert the XMCD's file")
    parser.add_argument('-p', '--prefix',
                        default='(SMATH)',
                        help='The prefix to output file')
    parser.add_argument('-s', '--sufix',
                        default='',
                        help='The sufix to output file')
    parser.add_argument('--ignore_custom',
                        action='store_true',
                        help='Include a "custom.sm" file into output XMCD directory with mathcad specific functions')
    parser.add_argument('-e', '--add_external',
                        action='extend',
                        default=[],
                        nargs='+',
                        help='Add user externals files into output XMCD directory. Try to add a file relative to "external_path", then try to get the file as full path. If a "*" is used, try to add all SM file in "external_path"')
    parser.add_argument('--external_path',
                        default='.',
                        help='The path to user external files')
    parser.add_argument('-f', '--filename',
                        default='',
                        help='Convert specific file')
    parser.add_argument('--smath_path',
                        default=r'C:\Program Files (x86)\SMath Studio',
                        help='Path to Smath Studio instalation, convert external files to SM when needed')
    parser.add_argument('--save_as_sm',
                        action='store_true',
                        help='Save output file as SM file')
    parser.add_argument('--gui',
                        action='store_true',
                        help='Open a gui version of script')
    args = parser.parse_args()
    mathcad2smath(args)


if __name__ == '__main__':
    main()
