#!/usr/bin/env python2.7
"""
	averageRelativeQE.py infile outfile

	Aim: Adds relative quantum efficiency

	Type averageRelativeQE.py -h to get help

	Version : $Rev: 514$
	
"""
from astropy.io import fits
from astropy.stats import sigma_clip
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import warnings;
import argparse
parser = argparse.ArgumentParser(epilog="""
    
    Version  : $Rev: 509 $
    Last Update: $Date: 2015-10-14 10:30:00 +0530 (Wen, 14 Oct 2015) $

""")
parser.add_argument("infile",help="File name containing relative qe file paths",type=str);
parser.add_argument("outfile",nargs="?",default="relativeQE.fits",help="Output Quantum Efficiency Map file name",type=str);
args=parser.parse_args();
warnings.simplefilter(action = "ignore", category = RuntimeWarning);
#------------------------------------------------------------------------------
data=np.zeros(((6,64,64)))
alldata=np.zeros(((6,64,64)))
allext=np.zeros(((6,128,128)))
numlines=0;
for line in open(args.infile,'r').readlines():
	print "Reading input file %s" %(line);
	numlines+=1;	
	line=line.replace("\n","");
	hdu=fits.open(line);
	for hdunum in range(1,6):
		if hdunum==5:
			allext[hdunum]+=hdu[hdunum].data;
		else:
			alldata[hdunum]+=data[hdunum];
			data[hdunum]=hdu[hdunum].data;
print "Addition complete"
hduout=fits.HDUList();
hduout.append(fits.ImageHDU());
hdu=fits.open(line);
for hdunum in range(1,6):
	#alldata[hdunum]/=numlines;

	if hdunum==5:
		hduout.append(fits.ImageHDU(allext[hdunum],hdu[hdunum].header));
	else:
		hduout.append(fits.ImageHDU(alldata[hdunum],hdu[hdunum].header));
hduout.writeto(args.outfile);
print "Wrote output to %s"%(args.outfile);	
