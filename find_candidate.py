import numpy as np
from glob import glob
import matplotlib.pyplot as plt

#data_dir = '/disk/dawn-1/sgiri/ML_project/ML_fesc/CLASH_data'
#lens_fol = glob(data_dir+'/ABELL*')+glob(data_dir+'/MACS*')+glob(data_dir+'/RXJ*')+glob(data_dir+'/MS*')+glob(data_dir+'/CL*')
#mags_fol = glob(data_dir+'/high_magnification/*')

#lens_names = [s.split('/')[-1] for s in lens_fol]
#mags_names = [s.split('/')[-1] for s in mags_fol]

#lens_var = []
#mags_var = []

def histogram_z_range(data_all, zl, zh=1000, bins=10, stel=0.2, z_pos=115):
	data_all = data_all[data_all[:,7]<stel]
	data_z = data_all[:,z_pos]
	data_z = data_z[data_z>=zl]
	data_z = data_z[data_z<=zh]
	ht = np.histogram(data_z, bins=bins)
	return ht[1][:-1], ht[0]

def show_hist_z_range(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=1000, bins=10, stel=0.2):
	assert camera[0] or camera[1] == 1
	lens_names = [s.split('/')[-1] for s in lens_fol]
	mags_names = [s.split('/')[-1] for s in mags_fol]
	ll = np.argwhere(lens_var==1)
	mm = np.argwhere(mags_var==1)
	to = 0
	if ll.size:
		for l in ll:
			filea = glob(lens_fol[l]+'/*_acs*')
			filei = glob(lens_fol[l]+'/*_ir*')
			z_pos = get_var_pos(filea[0], 'zb')
			data_a, data_i = 0, 0
			if camera[0]: data_a = np.loadtxt(filea[0])
			if camera[1]: data_i = np.loadtxt(filei[0])
			if camera[0] and camera[1]:
				data = np.vstack((data_a,data_i))
			else: data = data_a*camera[0]+data_i*camera[1]
			xx,yy = histogram_z_range(data, zl, zh=zh, bins=bins, stel=stel, z_pos=z_pos)
			plt.step(xx,yy, label=lens_names[l])
			to = to + np.sum(yy)
	if mm.size:
		for m in mm:
			filea = glob(mags_fol[m]+'/*_acs*')
			filei = glob(mags_fol[m]+'/*_ir*')
			z_pos = get_var_pos(filea[0], 'zb')
			data_a, data_i = 0, 0
			if camera[0]: data_a = np.loadtxt(filea[0])
			if camera[1]: data_i = np.loadtxt(filei[0])
			if camera[0] and camera[1]:
				data = np.vstack((data_a,data_i))
			else: data = data_a*camera[0]+data_i*camera[1]
			xx,yy = histogram_z_range(data, zl, zh=zh, bins=bins, stel=stel, z_pos=z_pos)
			plt.step(xx,yy, label=mags_names[m])
			to = to + np.sum(yy)
	plt.legend(loc=0)
	return to

def get_var_pos(filename, name):
	fo = open(filename, "rw+")
	lines = fo.readlines()
	i = 0
	while not name in lines[i].split(): i += 1
	lin = lines[i].split()
	var_pos = int(lin[lin.index(name)-1])
	return var_pos-1

def get_scatter_z(data_all, zl, zh=1000, stel=0.2, z_pos=115, f_pos=97):
	data_all = data_all[data_all[:,7]<stel]
	data_all = data_all[data_all[:,z_pos]<=zh]
	data_all = data_all[data_all[:,z_pos]>=zl]
	data_z = data_all[:,z_pos]
	data_f = data_all[:,f_pos]
	data_f_er = data_all[:,f_pos+1]
	data_z_lo = data_z-data_all[:,z_pos+1]
	data_z_hi = data_all[:,z_pos+2]-data_z
	#plt.errorbar(x, y, xerr=xerr, fmt='o')
	return data_f, data_z, data_f_er, data_z_lo, data_z_hi

def show_scatter_z(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=1000, stel=0.2, f_name='f105w'):
	assert camera[0] or camera[1] == 1
	lens_names = [s.split('/')[-1] for s in lens_fol]
	mags_names = [s.split('/')[-1] for s in mags_fol]
	ll = np.argwhere(lens_var==1)
	mm = np.argwhere(mags_var==1)
	to = 0
	if ll.size:
		for l in ll:
			filea = glob(lens_fol[l]+'/*_acs*')
			filei = glob(lens_fol[l]+'/*_ir*')
			z_pos = get_var_pos(filea[0], 'zb')
			f_pos = get_var_pos(filea[0], f_name+'_mag')
			data_a, data_i = 0, 0
			if camera[0]: data_a = np.loadtxt(filea[0])
			if camera[1]: data_i = np.loadtxt(filei[0])
			if camera[0] and camera[1]:
				data = np.vstack((data_a,data_i))
			else: data = data_a*camera[0]+data_i*camera[1]
			xx,yy,xerr,yerr1,yerr2 = get_scatter_z(data, zl, zh=1000, stel=0.2, z_pos=z_pos, f_pos=f_pos)
			plt.errorbar(xx,yy, xerr=xerr, yerr=[yerr1,yerr2], label=lens_names[l]+':'+str(xx.shape[0]), fmt='o')
			#to = xx.size
	if mm.size:
		for m in mm:
			filea = glob(mags_fol[m]+'/*_acs*')
			filei = glob(mags_fol[m]+'/*_ir*')
			z_pos = get_var_pos(filea[0], 'zb')
			f_pos = get_var_pos(filea[0], f_name+'_mag')
			data_a, data_i = 0, 0
			if camera[0]: data_a = np.loadtxt(filea[0])
			if camera[1]: data_i = np.loadtxt(filei[0])
			if camera[0] and camera[1]:
				data = np.vstack((data_a,data_i))
			else: data = data_a*camera[0]+data_i*camera[1]
			xx,yy,xerr,yerr1,yerr2 = get_scatter_z(data, zl, zh=1000, stel=0.2, z_pos=z_pos, f_pos=f_pos)
			plt.errorbar(xx,yy, xerr=xerr, yerr=[yerr1,yerr2], label=lens_names[l]+':'+str(xx.shape[0]), fmt='o')
			#to = xx.size
	plt.legend(loc=0)
	return to

