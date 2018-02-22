from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
import re
import fnmatch
path=sys.argv[1]
fig=plt.figure()

for orbit in os.listdir(path):
    if 'V' not in orbit:
            for mode in os.listdir(path+"/"+orbit):
                '''
                if re.search("modeSS", mode):
                    for file in os.listdir(path+"/"+orbit+"/modeSS"):
                        if fnmatch.fnmatch(file, '*.fits'):
                            org=fits.open(path+"/"+orbit+"/modeSS/"+file)
                            for i in range(1,5):
                                orgt = org[i].data["Time"]
                                size = len(orgt)
                                row_number = range(0,size)
                                #oh,b1=np.histogram(orgt,bins=(int)(orgt[-1]-orgt[0]))
                                plt.plot(row_number,orgt,color="red")
                                plt.xlabel('Row Number')
                                plt.ylabel('Time')
                                plt.title("Q"+str(i)+"_"+orbit+"_"+file)
                                plt.show()
                            org.close()
               '''
                if re.search("aux", mode):
                    '''
                    for file in os.listdir(path+"/"+orbit+"/aux"):
                        if fnmatch.fnmatch(file, '*.tct'):
                            org=fits.open(path+"/"+orbit+"/aux/"+file)
                            orgt = org[1].data["SPS_TIME"]
                            #oh,b1=np.histogram(orgt,bins=(int)(orgt[-1]-orgt[0]))
                            plt.plot(orgt,color="red")
                            plt.xlabel('Row Number')
                            plt.ylabel('SPS_TIME')
                            plt.title(orbit+"_"+file)
                            plt.show()
                            org.close()
                    '''
                    for file in os.listdir(path+"/"+orbit+"/aux/aux1"):
                        if fnmatch.fnmatch(file, '*.att'):
                            org=fits.open(path+"/"+orbit+"/aux/aux1/"+file)
                            roll_ra = org[1].data["ROLL_RA"]
                            size = len(roll_ra)
                            print size
                            row_number = range(0,size)
                            #print row_number
                            plt.plot(row_number,roll_ra,color="red")
                            plt.xlabel('Row Number')
                            plt.ylabel('ROLL_RA')
                            plt.title(orbit+"_"+file)
                            plt.show()

                            roll_dec = org[1].data["ROLL_DEC"]
                            plt.plot(row_number,roll_dec,color="red")
                            plt.xlabel('Row Number')
                            plt.ylabel('ROLL_DEC')
                            plt.title(orbit+"_"+file)
                            plt.show()

                            org.close()
