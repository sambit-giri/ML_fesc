import numpy as np
from glob import glob
from find_candidate_FF import get_obs_mags, get_var_pos, remove_limits, intrinsic_mag

data_dir = 'FrontierFields_data'
lens_fol = glob(data_dir+'/A2744*')+glob(data_dir+'/M0416*')

lens_names = [s.split('/')[-1] for s in lens_fol]

# Inputs
mock_catalogue_name = 'A2744cl'
lam_rest = 1500.

# Run
data_fol = lens_fol[lens_names.index(mock_catalogue_name)]

filez  = glob(data_fol+'/*_ZPHOT.cat')[0]
filea  = glob(data_fol+'/*_A.cat')[0]
z_pos  = get_var_pos(filez, 'zbest')
data_z = np.loadtxt(filez)[:,z_pos:z_pos+3]
data_o = np.loadtxt(filea)[:data_z.shape[0],:5]
data_a = get_obs_mags(filea, data_z[:,0], lam_rest)
dat_z, dat_a, dat_o = remove_limits(data_z, data_a, data_o, 5, zh=12.5, fl=20, fh=30, with_err=True)
dat_ai = intrinsic_mag(dat_a[:,0], dat_z[:,-1])

data_final = np.hstack((dat_o, dat_z, dat_a, dat_ai.reshape(-1,1)))

header = "ID\t #x\t #y\tRA\tDEC\tz_best\tz_err\tmagnif\tMAG1500_obs\tMAG1500_err\tMAG1500_int"
np.savetxt('output/mock_catalogue_'+mock_catalogue_name+'.cat', data_final, header=header, fmt='%1.3e')

print data_final.shape[0]


