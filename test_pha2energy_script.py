from astropy.io import fits
import numpy as np
import sys
#orghdr=fits.open("/data2/czti/testarea/Mayuri/release1.1_test_406/20160331_T01_112T01_9000000406_level2_original/czti/modeM0/AS1T01_112T01_9000000406cztM0_level2_bc.evt")
#newhdr=fits.open("/data2/czti/testarea/Mayuri/release1.1_test_406/20160331_T01_112T01_9000000406_level2/20160331_T01_112T01_9000000406_level2/czti/modeM0/AS1T01_112T01_9000000406cztM0_level2_bc.evt")
orghdr=fits.open(sys.argv[1])
newhdr=fits.open(sys.argv[2])
col=sys.argv[3]
quadsToBeProcess=int(sys.argv[4])
for qid in range(1,quadsToBeProcess):
    oe=orghdr[qid].data[col]
    ne=newhdr[qid].data[col]
    diff=np.max(oe-ne)
    print(diff)

'''
qid=1
oe=orghdr[qid].data[col]
ne=newhdr[qid].data[col]
diff1=np.max(oe-ne)
qid=2
oe=orghdr[qid].data[col]
ne=newhdr[qid].data[col]
diff2=np.max(oe-ne)
qid=3
oe=orghdr[qid].data[col]
ne=newhdr[qid].data[col]
diff3=np.max(oe-ne)
qid=4
oe=orghdr[qid].data[col]
ne=newhdr[qid].data[col]
diff4=np.max(oe-ne)
print(diff1)
print(diff2)
print(diff3)
print(diff4)
'''
