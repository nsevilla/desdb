#!/usr/bin/env python
"""
    %prog [options] fits_file table_name control_file

Convert the fits file to an ascii control file that can be loaded
into a database table using sqlldr

Optionally write the create table statement.
"""

import sys
from sys import stdin,stdout
import desdb


from optparse import OptionParser
parser=OptionParser(__doc__)
parser.add_option('--bands',default=None,
                  help=("comma separated list of band characters, "
                        "to convert index number to band characer "
                        "for arrays that contain band-dependent info.
                        " for example g,r,i,z"))
parser.add_option('--band-cols',default=None,
                  help=("comma separated list of array columns that "
                        "contain band-dependent information.  The "
                        "bands keyword is used to convert index name "
                        "to band character for these columns"))
parser.add_option('--ext',default=None,
                  help=("extension to read.  Default is first with data"))

parser.add_option('--create',action='store_true',
                  help=("write the create table statement to control_file.sql"))

def read_data(filename, ext=None):
    try:
        import fitsio
        data=fitsio.read(filename, ext=ext)
    except:
        try:
            # ....hate ....pyfits
            import pyfits
            ext_num,ext_string=get_ext(ext)
            if ext_num is not None:
                data=pyfits.getdata(filename, ext=ext_num)
            else:
                data=pyfits.getdata(filename, extname=ext_string)
        except:
            raise ImportError("could not import fitsio or pyfits")

    return data

def csv2list(data):
    if data is not None:
        data=[d for d in data.split(',')]

    return data

def get_ext(ext_string):
    """
    For pyfits stupidity
    """
    try:
        ext_num=int(ext_string)
    except:
        ext_num=None

    return ext_num, ext_string

def main():

    options,args = parser.parse_args(sys.argv[1:])
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    fits_file=args[0]
    table_name=args[1]
    control_file=args[2]

    bands=csv2list(options.bands)
    band_cols=csv2list(options.band_cols)

    data=read_data(fits_file, ext=options.ext)

    desdb.desdb.array2table(data, table_name, control_file,
                            bands=bands,
                            band_cols=band_cols,
                            create=options.create)

if __name__=="__main__":
    main()
