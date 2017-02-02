import numpy as np
from glob import glob
import matplotlib.pyplot as plt


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
			l = l[0]
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
			m = m[0]
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
	plt.ylabel('n(z)')
	plt.xlabel('z')
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

def get_scatter_z(data_all, zl, zh=1000, stel=0.2, z_pos=115, f_pos=97, with_err=None):
	data_all = data_all[data_all[:,7]<stel]
	if with_err:
		data_all = data_all[data_all[:,z_pos+2]<=zh]
		data_all = data_all[data_all[:,z_pos+1]>=zl]
	else:
		data_all = data_all[data_all[:,z_pos]<=zh]
		data_all = data_all[data_all[:,z_pos]>=zl]
	data_z = data_all[:,z_pos]
	data_f = data_all[:,f_pos]
	data_f_er = data_all[:,f_pos+1]
	data_z_lo = data_z-data_all[:,z_pos+1]
	data_z_hi = data_all[:,z_pos+2]-data_z
	return data_f, data_z, data_f_er, data_z_lo, data_z_hi

def show_scatter_z(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=1000, stel=0.2, f_name='f105w', xlim_l=None, xlim_r=None, with_err=None):
	assert camera[0] or camera[1] == 1
	lens_names = [s.split('/')[-1] for s in lens_fol]
	mags_names = [s.split('/')[-1] for s in mags_fol]
	ll = np.argwhere(lens_var==1)
	mm = np.argwhere(mags_var==1)
	to = 0
	if ll.size:
		for l in ll:
			l = l[0]
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
			xx,yy,xerr,yerr1,yerr2 = get_scatter_z(data, zl, zh=zh, stel=stel, z_pos=z_pos, f_pos=f_pos, with_err=with_err)
			num0 = xx.shape[0]; num=num0
			if xlim_l: num1 = xx[xx>=xlim_l].shape[0];num=num1
			if xlim_r: num2 = xx[xx<=xlim_r].shape[0];num=num2
			if xlim_l and xlim_r: num = num1+num2-num0
			plt.errorbar(xx,yy, xerr=xerr, yerr=[yerr1,yerr2], label=lens_names[l]+'('+str(num)+')', fmt='o')
			#to = xx.size
	if mm.size:
		for m in mm:
			m = m[0]
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
			xx,yy,xerr,yerr1,yerr2 = get_scatter_z(data, zl, zh=zh, stel=stel, z_pos=z_pos, f_pos=f_pos, with_err=with_err)
			num0 = xx.shape[0]; num=num0
			if xlim_l: num1 = xx[xx>=xlim_l].shape[0];num=num1
			if xlim_r: num2 = xx[xx<=xlim_r].shape[0];num=num2
			if xlim_l and xlim_r: num = num1+num2-num0
			plt.errorbar(xx,yy, xerr=xerr, yerr=[yerr1,yerr2], label=mags_names[m]+'('+str(num)+')', fmt='o')
			#to = xx.size
	plt.xlim(xlim_l,xlim_r)
	#plt.ylim(bottom=zl-1)
	plt.xlabel('m')
	plt.ylabel('z')
	plt.legend(loc=0)
	return to

def get_object_details(data_all, zl, zh=1000, stel=0.2, z_pos=115, f_pos=97, xlim_l=None, xlim_r=None, with_err=None):
	data_all = data_all[data_all[:,7]<stel]
	if with_err:
		data_all = data_all[data_all[:,z_pos+2]<=zh]
		data_all = data_all[data_all[:,z_pos+1]>=zl]
	else:
		data_all = data_all[data_all[:,z_pos]<=zh]
		data_all = data_all[data_all[:,z_pos]>=zl]
	if xlim_r: data_all = data_all[data_all[:,f_pos]<=xlim_r]
	if xlim_l: data_all = data_all[data_all[:,f_pos]>=xlim_l]
	return np.hstack((data_all[:,:5],np.expand_dims(data_all[:,z_pos],axis=1)))
	

def show_object_details(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=1000, stel=0.2, f_name='f105w', xlim_l=None, xlim_r=None, with_err=None):
	assert camera[0] or camera[1] == 1
	lens_names = [s.split('/')[-1] for s in lens_fol]
	mags_names = [s.split('/')[-1] for s in mags_fol]
	ll = np.argwhere(lens_var==1)
	mm = np.argwhere(mags_var==1)
	to = 0
	if ll.size:
		for l in ll:
			l = l[0]
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
			data = get_object_details(data, zl, zh=zh, stel=stel, z_pos=z_pos, f_pos=f_pos, xlim_l=xlim_l, xlim_r=xlim_r, with_err=with_err)
			print lens_names[l]
			print 'ID\tRA\tDec\tx\ty\tzb'
			if data.size: 
				for i in xrange(data.shape[0]): print data[i,:]
	if mm.size:
		for m in mm:
			m = m[0]
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
			data = get_object_details(data, zl, zh=zh, stel=stel, z_pos=z_pos, f_pos=f_pos, xlim_l=xlim_l, xlim_r=xlim_r, with_err=with_err)
			print mags_names[m]
			print 'ID\tRA\tDec\tx\ty\tzb'
			if data.size: 
				for i in xrange(data.shape[0]): print data[i,:]
	return 0

