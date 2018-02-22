#!/usr/bin/env python2.7
"""
	cross_correlate.py infile outfile

	Aim: Generate a cross correlation image

	Type cross_correlate.py -h to get help

	Version : $Rev: 514$
	
"""
from scipy import stats
from astropy.io import fits
from astropy.stats import sigma_clip
from scipy.optimize import curve_fit
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import warnings;
import argparse

#-----------function definations----------------------------------#
def fitme(x,m,c):
	return m*x+c




parser = argparse.ArgumentParser(epilog="""
    
    Version  : $Rev: 514 $
    Last Update: $Date: 2015-10-16 10:30:00 +0530 (Fri, 16 Oct 2015) $
    Ver 1.0: Basic code to calculate cross correlation
    Ver 1.1:  Added functionality to ignore the badpixels (2 Feb 2016)
    Ver 1.2:  Added functionality to generate chisquare matrix (3 Feb 2016)	

""")
parser.add_argument("infile",help="Input Detector Plane Histogram (DPH) file name",type=str);
parser.add_argument("shadowlibfile",help="Input shadow library file",type=str);
parser.add_argument("badpixfile",nargs="?", default="badpix.fits",help="Input baxpixel file name",type=str);
parser.add_argument("outfile",nargs="?",default="output.img",help="Output image name",type=str);
args=parser.parse_args();

chisqoutput=args.outfile+".chisq"
corroutput=args.outfile+".corr"
if(os.path.exists(corroutput)):
	os.remove(corroutput);
	os.remove(chisqoutput);
#-------------------parsing the input arguments----------------------------------------#
dph_hdu=fits.open(args.infile)
lib_hdu=fits.open(args.shadowlibfile);
badpix_hdu=fits.open(args.badpixfile)

fits.writeto(corroutput, dph_hdu[0].data, dph_hdu[0].header)
fits.writeto(chisqoutput, dph_hdu[0].data, dph_hdu[0].header)

resol=1.0
#---------------------initalization of variables-------------------------------------#
tx_range=np.arange(-3,3.1,0.1)
ty_range=np.arange(-3,3.1,0.1)
txwidth=np.shape(tx_range)
tywidth=np.shape(ty_range)
all_corr=np.zeros((txwidth[0], tywidth[0]))
print "Input file :%s"%(args.infile)
#print "Mask file :%s"%(args.maskfile)
print "Bad pix file :%s"%(args.badpixfile)
print "Output file : %s"%(args.outfile)
for hdunum in range(1,5):
	print "Processing HDU %d"%(hdunum)
	dph=dph_hdu[hdunum].data
	quad='Q'+str(hdunum-1)	
	shadowlib=lib_hdu[1].data[quad]
	badpix=badpix_hdu[hdunum].data;
	
	#converting detid,pixid to detx,dety
	detx = (((badpix['DETID'] % 4)*16) + (badpix['PIXID'] % 16))
	dety = (((badpix['DETID'] / 4)*16) + (badpix['PIXID'] / 16))
	flags = np.zeros((64,64))
	if(hdunum-1==0 or hdunum-1==3):
		dety=63-dety;
	flags[dety,detx] = badpix['PIX_FLAG']
	dph_=np.where(((flags!=0) | (dph==0)),np.nan,dph);
	dph_=dph_[~np.isnan(dph_)]
	corr=np.zeros((txwidth[0], tywidth[0]))
	chisq_matrix=np.zeros((txwidth[0], tywidth[0]))
	i=0;
	j=0;
	qid=hdunum-1
	
	#1923
	counter=0;
	for tx in tx_range:
		j=0;
		for ty in ty_range:
			shadow=np.reshape(shadowlib[counter],((64,64)));
			shadow_=np.where(((flags!=0) | (dph==0))   ,np.nan,shadow);
			shadow_=shadow_[~np.isnan(shadow_)]
			counter=counter+1;	
			
			##code to calculate cross correlation
			cshadow_=1-shadow_
			corrmat=shadow_*dph_
			ccorrmat=cshadow_*dph_

			corrsum=np.nansum(corrmat)
			ccorrsum=np.nansum(ccorrmat)
			norm=np.nansum(shadow_);
			cnorm=np.nansum(cshadow_);
			if norm !=0.0:
				corr[i][j]=(corrsum/norm)-(ccorrsum/cnorm);
				all_corr[i][j]+=corr[i][j];
			else:
				corr[i][j]=0;


			##code to calculate chisq matrix
			dof=shadow_.size-2
			#out,tmp = curve_fit(fitme,shadow_, dph_)
			#y=fitme(shadow_,out[0],out[1]) 
			slope, intercept, r_value, p_value, std_err = stats.linregress(shadow_,dph_)
			y=fitme(shadow_,slope,intercept) 
			deltasq =(dph_ - y)**2 / sqrt(dph_)
			chisq = np.sum(deltasq)/dof
			chisq_matrix[i][j]=chisq;	
			j+=1
		i+=1	
	fits.append(corroutput,corr);
	fits.append(chisqoutput,chisq_matrix);

	 
	#plt.imshow(corr,interpolation='nearest',cmap='jet',vmin=np.min(corr),vmax=np.max(corr),origin='lower');
	#if qid==0:
	#	plt.colorbar();
	#plt.show();
	outfile="cyg_output_"+`qid`+".png";
	plt.savefig(outfile);
fits.append(corroutput,all_corr);
