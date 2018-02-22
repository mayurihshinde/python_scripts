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
	
	tbdata = hdulist[hdunum].data
	time = tbdata.field('time') 
	cztseccnt = tbdata.field('cztseccnt') 
	frameno = tbdata.field('frameno') 
	
	framediff=np.diff(frameno)
	np.where(framediff==0)
	plt.xlabel("Row Number")
	plt.ylabel("Frame Difference")
	plt.title("Difference of frameno")
	plt.plot(framediff)
	frame_file = os.path.basename(sys.argv[1]).replace('.hdr','_framediff.jpg')
	frameoutput='/data2/czti/testarea/Mayuri/crabPhaseSingleEvents/check_hdr/'+frame_file
	print(frameoutput)
	plt.savefig(frameoutput)
	#plt.show()
	
	cztseccntdiff=np.diff(cztseccnt)
	np.where(cztseccntdiff==0)
	plt.xlabel("Row Number")
	plt.ylabel("cztsec count Difference")
	plt.title("Difference of cztsec count ")
	plt.plot(cztseccntdiff)
	seccnt_file = os.path.basename(sys.argv[1]).replace('.hdr','_seccntdiff.jpg')
	seccntoutput='/data2/czti/testarea/Mayuri/crabPhaseSingleEvents/check_hdr/'+seccnt_file
	print(seccntoutput)
	plt.savefig(seccntoutput)
	
