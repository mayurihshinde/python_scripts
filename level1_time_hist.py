#!/usr/bin/python
from astropy.io import fits
import sys
import numpy as np
import matplotlib.pyplot as plt
import os.path
 
total = len(sys.argv)
cmdargs = str(sys.argv)


if total < 2:
   print("Input header file is required.")

else:		
	hdulist = fits.open(sys.argv[1])
	
	hdunum=1
	
	for hdunum in range(1,5):
		tbdata = hdulist[hdunum].data
		time = tbdata.field('time') 
	
		h,b=np.histogram(time,bins=int(time[-1]-time[0]))
		plt.plot(h)
		time_file = os.path.basename(sys.argv[1]).replace('.fits','_time_hist_'+str(hdunum)+'.jpg')
		timeoutput='/data2/czti/testarea/Mayuri/crabPhaseSingleEvents/check_hdr/'+time_file
		print(timeoutput)
		plt.savefig(timeoutput)
