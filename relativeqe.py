#!/usr/bin/env python2.7
"""
	relativeqe.py infile outfile

	Aim: Calculate relative quantum efficiency

	Type relativeqe -h to get help

	Version : $Rev: 509$
	
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
parser.add_argument("infile",help="Detector Plane Histogram (DPH) file to be used for processing",type=str);
parser.add_argument("badpixfile",nargs="?",help="Input badpixel file in binary table format",type=str);
parser.add_argument("outfile",nargs="?",default="qemap.pdf",help="Output Quantum Efficiency Map file name",type=str);
args=parser.parse_args();
warnings.simplefilter(action = "ignore", category = RuntimeWarning);
#------------------------------------------------------------------------------
#Opening dph file for reading
hdu=fits.open(args.infile);
badpixhdu=fits.open(args.badpixfile);
#Creating output pdf file
pp=PdfPages(args.outfile);
width=2.46;
width=2.31;
hduout=fits.HDUList();
hduout.append(fits.ImageHDU());
#Iterate through all quadrants
for hdunum in range(1,5):
	#reading badpixel file
	badpix=badpixhdu[hdunum].data;
	#converting detid,pixid to detx,dety
	detx = (((badpix['DETID'] % 4)*16) + (badpix['PIXID'] % 16))
	dety = (((badpix['DETID'] / 4)*16) + (badpix['PIXID'] / 16))
	flags = np.zeros((64,64))
	if(hdunum-1==0 or hdunum-1==3):
		dety=63-dety;
	flags[dety,detx] = badpix['PIX_FLAG']
	print "Reading HDU %d" % (hdunum);
	#reading dph
	quad=hdu[hdunum].data;
	for i in range (0,64):
		if i%16 == 0 or i%16==15:
			width=2.31
		else:
			width=2.46
		for j in range (0,64):
			if i%16 == 0 or i%16==15:
				height=2.31
			else:
				height=2.46
			quad[i][j]/=(width*height);




	#removing disabled pixels
	quad=np.where(flags==4,np.nan,quad);
	#removing pixels with zero counts
	quad_=np.where(quad==0,np.nan,quad)
	clip_mean=0;
	oldmean=0.0;
	clip_sigma=0;
	while True:
		#calculating mean
		clip_mean=np.nanmean(quad_);
		#calculating sigma
		clip_sigma=np.nanstd(quad_);
		#removing pixels with counts > 5sigma
		quad_=np.where(quad_>clip_mean+(5*clip_sigma),np.nan,quad_);
		if np.fabs(clip_mean-oldmean)<0.01:
			break;
		oldmean=clip_mean;
#	print "sigma clipped mean: %f\tclipped sigma %f" %(clip_mean,clip_sigma);
	#dividing with sigma clipped mean
	quad_/=np.nanmean(quad_);
	#plotting image
	plt.imshow(quad_,interpolation='nearest',cmap='jet',vmin=np.nanmin(quad_),vmax=np.nanmax(quad_),origin='lower');
	#adding color bar to plot
	if hdunum == 1:
		plt.colorbar();
	#saving plot	
	plt.savefig(pp,format='pdf');
	hduout.append(fits.ImageHDU(quad_));
#closing output pdf file
pp.close();
plt.close();
outfits=args.outfile.replace("pdf","fits");
hduout.writeto(outfits);
print "Execution complete"
#x=np.where(quad_clipped.mask==False,quad_clipped.data,-1)
#img = pyplot.imshow(data,interpolation='nearest',cmap ='jet',vmin=-1,vmax=1)

