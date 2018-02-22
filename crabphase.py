#!/usr/bin/python
from astropy.io import fits
import numpy as np
import sys
import os

filename="/data2/czti/testarea/Mayuri/crabPhaseSingleEvents/crabphase.txt"
fobj = open(filename, 'a')
try:
    s = os.stat(filename)
    if s.st_size == 0:
        fobj.write('FileName\t\t\t\t\t\tHDUNumber\tOffpulseSum\tPulse1Sum\tPulse2Sum\tBridgeSum\tGrandTotal')
        
except OSError as e:
    print e
    

total = len(sys.argv)
cmdargs = str(sys.argv)


if total < 2:
   print "Input event file is required."

else:		
	hdulist = fits.open(str(sys.argv[1]))
	for hdunum in range(1,5):
		 
		tbdata = hdulist[hdunum].data
		energy=tbdata.field(11)
		weight=tbdata.field(15)
		phase=tbdata.field(13)
	
		#energy=tbdata['ENERGY']
		#weight=tbdata['WEIGHT']
		#phase=tbdata['PHASE']
	
		offpulse = []
		pulse1 = []
		pulse2 = []
		bridge = []
	
		for i in range(0,len(energy)):
			 if phase[i]>=0.05 and phase[i]<0.30:
	   		 	offpulse.append(energy[i]*weight[i])
	   		 elif phase[i]>= 0.30 and phase[i]<0.50:
	   		 	pulse1.append(energy[i]*weight[i])
	   		 elif phase[i]>= 0.90 or phase[i]<0.05:
	   		 	pulse2.append(energy[i]*weight[i])
	      		 elif phase[i]>= 0.50 and phase[i]<0.90:
	   		 	bridge.append(energy[i]*weight[i])
	      	
	      	offpulse_sum=sum(offpulse)
	      	pulse1_sum=sum(pulse1)
	      	pulse2_sum=sum(pulse2)
	      	bridge_sum=sum(bridge)
	      	
	      	total=offpulse_sum+pulse1_sum+pulse2_sum+bridge_sum
	      	
	        fobj.write("\n"+str(sys.argv[1])+"\t\t"+str(hdunum)+"\t"+str(offpulse_sum)+"\t"+str(pulse1_sum)+"\t"+str(pulse2_sum)+"\t"+str(bridge_sum)+"\t"+str(total))
              
