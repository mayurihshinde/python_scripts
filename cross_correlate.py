#!/usr/bin/env python2.7
"""
	cross_correlate.py infile outfile

	Aim: Generate a cross correlation image

	Type cross_correlate.py -h to get help

	Version : $Rev: 512$
	
"""

from astropy.io import fits
from astropy.stats import sigma_clip
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import warnings;
import argparse

dph_hdu=fits.open('/home/czti/ajay/crab_full.dph')
mask_hdu=fits.open('/home/czti/latest_CZTI_pipeline/CZTI/CALDB_20150106/astrosat/czti/bcf/CZTIMask64x64.fits')
badpix_hdu=fits.open('/home/czti/latest_CZTI_pipeline/CZTI/CALDB_20150106/astrosat/czti/bcf/AS1cztbadpix20150526v01.fits')	
hdunum=1;
dph=dph_hdu[hdunum].data
mask=mask_hdu[hdunum].data
badpix=badpix_hdu[hdunum].data;
#converting detid,pixid to detx,dety
detx = (((badpix['DETID'] % 4)*16) + (badpix['PIXID'] % 16))
dety = (((badpix['DETID'] / 4)*16) + (badpix['PIXID'] / 16))
flags = np.zeros((64,64))
if(hdunum-1==0 or hdunum-1==3):
	dety=63-dety;
flags[dety,detx] = badpix['PIX_FLAG']
dph_=np.where(flags==4,np.nan,dph);
mask_=np.where(flags==4,np.nan,mask);
corr=dph*mask
