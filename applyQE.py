#!/usr/bin/env python2.7
"""
	applyQE.py infile outfile

	Aim: Apply relative quantum efficiency to DPH

	Type applyQE.py -h to get help

	Version : $Rev: 514$
	
"""
from astropy.io import fits
import numpy as np
import warnings;
import argparse
parser = argparse.ArgumentParser(epilog="""
    
    Version  : $Rev: 514 $
    Last Update: $Date: 2015-10-16 10:30:00 +0530 (Fri, 16 Oct 2015) $

""")
parser.add_argument("infile",help="Input Detector Plane Histogram (DPH) file name",type=str);
parser.add_argument("relqefile",nargs="?",default="relativeQE.fits",help="Input relative qe file name",type=str);
parser.add_argument("outfile",nargs="?",default="output.dph",help="Output Detector Plane Histrogram file name",type=str);
args=parser.parse_args();
warnings.simplefilter(action = "ignore", category = RuntimeWarning);
#------------------------------------------------------------------------------
dphhdu=fits.open(args.infile);
qehdu=fits.open(args.relqefile);
fits.writeto(args.outfile, dphhdu[0].data, dphhdu[0].header)
for hdunum in range(1,5):
	dph=dphhdu[hdunum].data;
	qe=qehdu[hdunum].data
	dph=dph/qe;
	dph_=np.where(np.isnan(dph),0,dph)
	fits.append(args.outfile,dph_,dphhdu[hdunum].header);
#outhdu.writeto(args.outfile);
