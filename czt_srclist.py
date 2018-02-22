#!/usr/bin/env python2.7
"""
	czt_srclist.py 	RAPNT DECPNT BAT CATALOG

	Aim: List sources in CZTI field of view

	Type czt_srclist.py -g

	18 Aug 2016, Ajay Vibhute	
"""
from astropy.io import fits
import numpy as np
import warnings;
import subprocess
import argparse
parser = argparse.ArgumentParser(epilog="""
    

""")
parser.add_argument("RAPNT",help="Enter pointing RA",type=float);
parser.add_argument("DECPNT",help="Enter pointing DEC",type=float);
parser.add_argument("ROLLROT",help="Enter roll rot",type=float);
parser.add_argument("bat_catlog",nargs="?",help="Enter path for BAT catalog",type=str);
args=parser.parse_args();
catloghdu=fits.open(args.bat_catlog)
rapnt=args.RAPNT
decpnt=args.DECPNT
rollrot=args.ROLLROT
catlog=catloghdu[1].data
flux_threashold=2386.15/2.0
subcatlog=catlog[np.where(catlog['FLUX']>flux_threashold)]
commandbuff=""
output=[]
for entry in subcatlog:
	commandbuff="convert 1 "+str(rapnt) +" "+str(decpnt)+" "+str(rollrot) +" "+str(entry['RA'])+" "+ str(entry['DEC'])
	out=subprocess.Popen(commandbuff,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(stdout,stderr)=out.communicate()
	output.append(stdout.decode().split())
out=np.array(output)
theta=np.array(map(float,out[:,0]))
phi=np.array(map(float,out[:,1]))
tx=np.array(map(float,out[:,2]))
ty=np.array(map(float,out[:,3]))
src_sidemask_index=np.where(  ( (theta> 2) & (theta<88) & (phi>135) & (phi<225) ))
src_topmask_index=np.where((  (tx> -4) & ( tx<4) & ( ty>-4) &( ty<4) ) )
#print src_sidemask
#print src_topmask_index



#if len(src_topmask_index[0]) !=0:
#	print subcatlog[ src_topmask_index[0]]["RA"][0],subcatlog[ src_topmask_index[0]]["DEC"][0],subcatlog[ src_topmask_index[0]]["FLUX"][0]

if len(src_sidemask_index[0]) !=0:
	print  rapnt, decpnt,rollrot,subcatlog[ src_sidemask_index[0]]["RA"][0],subcatlog[ src_sidemask_index[0]]["DEC"][0],theta[src_sidemask_index][0],phi[src_sidemask_index][0]
	
	
#,subcatlog[ src_sidemask_index[0]]["FLUX"][0]
