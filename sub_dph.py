#!/usr/bin/env python2.7
"""
	
	Aim: subtracts second dph from first

	Type sub_dph.py -h to get help

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
parser.add_argument("dph1",help="First DPH",type=str);
parser.add_argument("dph2",help="Second DPH",type=str);
parser.add_argument("outfile",nargs="?",default="diff.fits",help="output file",type=str);
args=parser.parse_args();
warnings.simplefilter(action = "ignore", category = RuntimeWarning);

dph1=np.zeros(((1,0,0)))
dph2=np.zeros(((6,256,256)))
diff=np.zeros(((6,64,64)))

dph1_hdu=fits.open(args.dph1);
dph2_hdu=fits.open(args.dph2);
for hdunum in range(1,6):
	
	if hdunum==5:
		combined_diff=dph1_hdu[hdunum].data - dph2_hdu[hdunum].data
	else:
		diff[hdunum]=dph1_hdu[hdunum].data - dph2_hdu[hdunum].data


hduout=fits.HDUList();
hduout.append(fits.ImageHDU(dph1[0],dph1_hdu[0].header));
for hdunum in range(1,6):
	print("$$$$$$$$$$$hudnum:%d"%( hdunum));
	if hdunum==5:
		print "Appending full dpi"
		hduout.append(fits.ImageHDU(combined_diff,dph1_hdu[hdunum].header));
	else:
		hduout.append(fits.ImageHDU(diff[hdunum],dph1_hdu[hdunum].header));
hduout.writeto(args.outfile);

