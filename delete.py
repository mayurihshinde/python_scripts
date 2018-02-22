import numpy as np
import os.path
for i in os.listdir('/data2/czti/level1/20160331_T01_112T01_9000000406_level1/czti/orbit/'):
    if 'V' not in i:
        print(i)
