# mathcad2smath
Command tool to convert mathcad XMCD to XMCD with Smath Studio support

usage: mathcad2smath [-h] [-o] [-r] [-d BASEDIR] [-p PREFIX] [-s SUFIX] [--ignore_custom]
                     [-e ADD_EXTERNAL [ADD_EXTERNAL ...]] [--external_path EXTERNAL_PATH] [-f FILENAME]

Convert XMCD mathcad files into XMCD compatible with Smath Studio

optional arguments:
  -h, --help            show this help message and exit
  -o, --overwrite       Overwrite the output file if exist
  -r, --recursive       Find XMCD files recursively
  -d BASEDIR, --basedir BASEDIR
                        The basedir to convert the XMCD's file
  -p PREFIX, --prefix PREFIX
                        The prefix to output file
  -s SUFIX, --sufix SUFIX
                        The sufix to output file
  --ignore_custom       Include a "custom.sm" file into output XMCD directory with mathcad specific functions   
  -e ADD_EXTERNAL [ADD_EXTERNAL ...], --add_external ADD_EXTERNAL [ADD_EXTERNAL ...]
                        Add user externals files into output XMCD directory. Try to add a file relative to      
                        "external_path", then try to get the file as full path. If a "*" is used, try to add    
                        all SM file in "external_path"
  --external_path EXTERNAL_PATH
                        The path to user external files
  -f FILENAME, --filename FILENAME
                        Convert specific file
