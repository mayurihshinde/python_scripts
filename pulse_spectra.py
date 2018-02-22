#!/usr/bin/env python2.7
"""
	
	Aim: subtracts second dph from first

	Type pulse_spectra.py -h to get help

	Version : $Rev: $
	
"""
from astropy.io import fits
from astropy.stats import sigma_clip
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import warnings;
import argparse
import os
import powerlaw
parser = argparse.ArgumentParser(epilog="""
    
    Version  : $Rev:  $
    Last Update: $Date: 2016-01-01 11:30:00 +0530 $

""")
parser.add_argument("pulse_evt",help="Event file for pulse phase",type=str);
parser.add_argument("bg_evt",help="Event file for background phase",type=str);
parser.add_argument("outfile",nargs="?",default="spectra.txt",help="output file",type=str);
parser.add_argument("binsize",nargs="?",default=5,help="binsize",type=int);
parser.add_argument("start",nargs="?",default=25,help="binsize",type=int);
parser.add_argument("end",nargs="?",default=125,help="binsize",type=int);

args=parser.parse_args();
warnings.simplefilter(action = "ignore", category = RuntimeWarning);

startEnergy=args.start
endEnergy=args.end
energyBin=args.binsize
pulse_phase=0.58
bg_phase=0.28
nbins=((endEnergy-startEnergy)/energyBin);
pulse_hdu=fits.open(args.pulse_evt);
bg_hdu=fits.open(args.bg_evt);
x=np.zeros(nbins);
spec=np.zeros(nbins);
x_=np.zeros(nbins);
spec_=np.zeros(nbins);
error=np.zeros(nbins);
print "Start:",startEnergy
print "End:",endEnergy
print "Binsize:",energyBin
print "Numbins:",nbins;
ibin=0;
f = open(args.outfile, 'w')
for energy in range(startEnergy,endEnergy,energyBin):
	pulse_count=0;
	pulse_error=0;

	bg_count=0
	bg_error=0
	for hdunum in range(1,5):
		pulse_data=pulse_hdu[hdunum].data[np.where((pulse_hdu[hdunum].data['ENERGY']>energy) & (pulse_hdu[hdunum].data['ENERGY']<(energy+energyBin)) )]
		pulse_count+=(np.size(pulse_data)/pulse_phase)
		pulse_error+=np.size(pulse_data);
		
		bg_data=bg_hdu[hdunum].data[np.where((bg_hdu[hdunum].data['ENERGY']>energy) & (bg_hdu[hdunum].data['ENERGY']<(energy+energyBin)) )]
		bg_count+=(np.size(bg_data)/bg_phase)
		bg_error+=np.size(bg_data);
	x[ibin]=energy+energyBin/2.0
	spec[ibin]=pulse_count-bg_count;
	error[ibin]=np.sqrt( (pulse_error/(pulse_phase*pulse_phase))+(bg_error/(bg_phase*bg_phase)) )

	x_[ibin]=np.log10(x[ibin])
	spec_[ibin]=np.log10(spec[ibin])

	tmp=str(x[ibin])+"\t"+str(spec[ibin])+"\t"+str(error[ibin])+"\t"+str(x_[ibin])+"\t"+str(spec_[ibin])+"\t"+str(error[ibin]/spec[ibin])+"\n";
	#print tmp
	f.write(tmp);
	ibin+=1;
f.close();
x_=np.log10(x)
xspec_=np.log10(spec)
alpha=np.polyfit(x_,xspec_,1)
print alpha
