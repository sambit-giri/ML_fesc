import numpy as np
from glob import glob

data_dir = '/disk/dawn-1/sgiri/ML_project/ML_fesc/CLASH_data'
lens_fol = glob(data_dir+'/ABELL*')+glob(data_dir+'/MACS*')+glob(data_dir+'/RXJ*')+glob(data_dir+'/MS*')+glob(data_dir+'/CL*')+glob(data_dir+'/high_magnification/*')


