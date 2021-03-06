#!/usr/bin/python
from astropy.io import fits
import matplotlib.pyplot as plt

filename="/home/cztipoc/czti/trunk/users/mayuri/bash_script/data_loss_tele_error.txt"

with open(filename) as f:
	 lines = f.readlines()
    	 x = [line.split()[0] for line in lines]
    	 y = [line.split()[1] for line in lines]


fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Data loss due to telementory error")    
ax1.set_xlabel("Orbit Number")
ax1.set_ylabel("Data Loss")

ax1.plot(x,y, c='r')

leg = ax1.legend()

plt.show()


