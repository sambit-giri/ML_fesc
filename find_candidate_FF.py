import numpy as np
from glob import glob
import matplotlib.pyplot as plt

def filter_zeroth_flux(name):
	filters = ['B435','V606','I814','Y105','J125','JH140','H160','IRAC1', 'IRAC2']
	fluxes  = [4040., 3233., 2414.5, 1975.16, 1564.25, 1324.81, 1138.06, 277.22, 179.04]
	return fluxes[filters.index(name.upper)]


def histogram_z_range(data_all, zl, zh=1000, bins=10, z_pos=115):
	data_z = data_all[:,z_pos]
	data_z = data_z[data_z>=zl]
	data_z = data_z[data_z<=zh]
	ht = np.histogram(data_z, bins=bins)
	return ht[1][:-1], ht[0]

def show_hist_z_range(lens_fol, lens_var, zl, zh=1000, bins=10):
	lens_names = [s.split('/')[-1] for s in lens_fol]
	ll = np.argwhere(lens_var==1)
	to = 0
	if ll.size:
		for l in ll:
			l = l[0]
			filez = glob(lens_fol[l]+'/*_ZPHOT.cat')
			#filea = glob(lens_fol[l]+'/*_A.cat')
			z_pos = get_var_pos(filez[0], 'zbest')
			data_z = np.loadtxt(filez[0])
			#data_a = np.loadtxt(filei[0])
			xx,yy = histogram_z_range(data_z, zl, zh=zh, bins=bins, z_pos=z_pos)
			plt.step(xx,yy, label=lens_names[l])
			to = to + np.sum(yy)
	plt.ylabel('n(z)')
	plt.xlabel('z')
	plt.legend(loc=0)
	return to

def get_var_pos(filename, name):
	fo = open(filename, "rw+")
	lines = fo.readlines()
	lin = lines[0].split()
	var_pos = lin.index(name.upper())-1
	return var_pos

def show_scatter_z(lens_fol, lens_var, zl, zh=1000, f_name='Y105', xlim_l=None, xlim_r=None, with_err=None):
	lens_names = [s.split('/')[-1] for s in lens_fol]
	ll = np.argwhere(lens_var==1)
	to = 0
	if ll.size:
		for l in ll:
			l = l[0]
			filez  = glob(lens_fol[l]+'/*_ZPHOT.cat')
			filea  = glob(lens_fol[l]+'/*_B.cat')
			z_pos  = get_var_pos(filez[0], 'zbest')
			f_pos  = get_var_pos(filea[0], 'FLUX_'+f_name)
			fr_pos = get_var_pos(filea[0], 'FLUXERR_'+f_name)
			data_z = np.loadtxt(filez[0])[:,z_pos:z_pos+2]
			data_m = np.loadtxt(filea[0])
			data_m = np.vstack((data_m[:,f_pos],data_m[:,fr_pos])).T
			xx,yy,xerr,yerr1,yerr2 = get_scatter_z(data_z, data_m, zl, zh=zh, z_pos=z_pos, f_pos=f_pos, fr_pos=fr_pos, with_err=with_err)
			num0 = xx.shape[0]; num=num0
			if xlim_l: num1 = xx[xx>=xlim_l].shape[0];num=num1
			if xlim_r: num2 = xx[xx<=xlim_r].shape[0];num=num2
			if xlim_l and xlim_r: num = num1+num2-num0
			plt.errorbar(xx,yy, xerr=xerr, yerr=[yerr1,yerr2], label=lens_names[l]+'('+str(num)+')', fmt='o')
			#to = xx.size
	
	plt.xlim(xlim_l,xlim_r)
	#plt.ylim(bottom=zl-1)
	plt.xlabel('m')
	plt.ylabel('z')
	plt.legend(loc=0)
	return to

def get_scatter_z(data_z, data_a, zl, zh=zh, z_pos=z_pos, f_pos=f_pos, fr_pos=fr_pos, with_err=with_err):
	if with_err:
		up = np.argwhere(data_z[:,0]+data_z[:,1]<=zh)
		data_z = data_z[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]-data_z[:,1]>=zl)
		data_z = data_z[np.squeeze(dn)]
	else:
		up = np.argwhere(data_z[:,0]<=zh)
		data_z = data_z[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]>=zl)
		data_z = data_z[np.squeeze(dn)]
	data_z = data_all[:,z_pos]
	data_f = data_all[:,f_pos]
	data_f_er = data_all[:,f_pos+1]
	data_z_lo = data_z-data_all[:,z_pos+1]
	data_z_hi = data_all[:,z_pos+2]-data_z
	return data_f, data_z, data_f_er, data_z_lo, data_z_hi

