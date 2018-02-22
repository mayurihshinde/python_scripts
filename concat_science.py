#!/usr/bin/env python2.7
"""
	concat_science.py indir

	Aim: Concats all the level1 science file
	
	Type concat_science.py -h to get help

	Version : $Rev: 540$
	
"""
from astropy.io import fits
import numpy as np
import warnings;
import argparse
import os;
parser = argparse.ArgumentParser(epilog="""
    
    Version  : $Rev: 540 $
    Last Update: $Date: 2015-11-17 11:30:00 +0530$

""")
parser.add_argument("indir",help="Input level1 directory name including czti",type=str);
args=parser.parse_args();
p=os.popen("find " +args.indir +" -name *.fits");
arr_fits_files=p.read().split("\n");
del arr_fits_files[-1]

for file in arr_fits_files:
	tmp=file.split("/");
#	print tmp[len(tmp)-1], tmp[len(tmp)-2]
	modedir=args.indir+"/"+ tmp[len(tmp)-2]
	if not os.path.exists(modedir):
		os.makedirs(modedir);
	outfile=args.indir+"/"+ tmp[len(tmp)-2]+"/"+tmp[len(tmp)-1]
	#print outfile
	if not os.path.exists(outfile):
		os.system("cp "+file+" "+ outfile);
	else:
		for hduno in range(1,7):
			t1 = fits.open(file);
			t2 = fits.open(outfile);
			nrows1 = t1[hduno].data.shape[0]
			nrows2 = t2[hduno].data.shape[0]
			nrows = nrows1 + nrows2
			hdu = fits.BinTableHDU.from_columns(t1[hduno].columns, nrows=nrows)
			hdu.header=t1[hduno].header	
			for colname in t1[hduno].columns.names:
				hdu.data[colname][nrows1:] = t2[hduno].data[colname]
			#fits.update(outfile,hdu.data,ext=hduno);	
			fits.append('test.fits',hdu.data,hdu.header);
			t1.close()
			t2.close()
		os.system('mv test.fits' +" "+outfile);
