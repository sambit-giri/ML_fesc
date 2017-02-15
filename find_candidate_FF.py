import numpy as np
from glob import glob
import matplotlib.pyplot as plt

def filter_zeroth_flux(name):
	filters = ['B435','V606','I814','Y105','J125','JH140','H160','IRAC1', 'IRAC2']
	fluxes  = [4040., 3233., 2414.5, 1975.16, 1564.25, 1324.81, 1138.06, 277.22, 179.04]
	return fluxes[filters.index(name.upper)]

def get_filter_name(lam_rest, z):
	filters    = np.array(['B435','V606','I814','Y105','J125','JH140','H160','IRAC1', 'IRAC2'])
	filter_lam = np.array([4350., 6060., 8140., 10500., 12500., 14000., 16000., 36000., 45000.])
	obs_lam    = lam_rest*(1+z)
	return filters[np.abs(filter_lam-obs_lam).argmin()]

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

def show_scatter_z(lens_fol, lens_var, zl, zh=1000, lam_rest=1500., xlim_l=None, xlim_r=None, with_err=None):
	lens_names = [s.split('/')[-1] for s in lens_fol]
	ll = np.argwhere(lens_var==1)
	to = 0
	if ll.size:
		for l in ll:
			l = l[0]
			filez  = glob(lens_fol[l]+'/*_ZPHOT.cat')
			filea  = glob(lens_fol[l]+'/*_A.cat')
			z_pos  = get_var_pos(filez[0], 'zbest')
			#f_pos  = get_var_pos(filea[0], 'MAG_'+f_name)
			#fr_pos = get_var_pos(filea[0], 'MAGERR_'+f_name)
			data_z = np.loadtxt(filez[0])[:,z_pos:z_pos+2]
			#data_m = np.loadtxt(filea[0])
			#data_m = np.vstack((data_m[:,f_pos],data_m[:,fr_pos])).T
			data_m = get_obs_mags(filea[0], data_z[:,0], lam_rest)
			xx,yy,xerr,yerr = get_scatter_z(data_z, data_m, zl, zh=zh, fl=xlim_l, fh=xlim_r, with_err=with_err)
			num0 = xx.shape[0]; num=num0
			#if xlim_l: num1 = xx[xx>=xlim_l].shape[0];num=num1
			#if xlim_r: num2 = xx[xx<=xlim_r].shape[0];num=num2
			#if xlim_l and xlim_r: num = num1+num2-num0
			plt.errorbar(xx,yy, xerr=xerr, yerr=yerr, label=lens_names[l]+'('+str(num)+')', fmt='o')
	
	#plt.xlim(xlim_l,xlim_r)
	#plt.ylim(bottom=zl-1)
	plt.xlabel('m')
	plt.ylabel('z')
	plt.legend(loc=0)
	return to

def get_obs_mags(file_name, zs, lam_rest):
	f_names  = [get_filter_name(lam_rest, z) for z in zs]
	f_poses  = [get_var_pos(file_name, 'MAG_'+f_name) for f_name in f_names]
	fr_poses = [get_var_pos(file_name, 'MAGERR_'+f_name) for f_name in f_names]
	data_m = np.zeros((len(zs),2))
	data   = np.loadtxt(file_name)
	for i in xrange(len(zs)):
		data_m[i,0] = data[i,f_poses[i]]
		data_m[i,1] = data[i,fr_poses[i]]
	return data_m

def get_scatter_z(data_z, data_a, zl, zh=100, fl=15, fh=30, with_err=None):
	if with_err:
		up = np.argwhere(data_z[:,0]+data_z[:,1]<=zh)
		data_z = data_z[np.squeeze(up)]
		data_a = data_a[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]-data_z[:,1]>=zl)
		data_z = data_z[np.squeeze(dn)]
		data_a = data_a[np.squeeze(dn)]
		if fh:
			up = np.argwhere(data_a[:,0]+data_a[:,1]<=fh)
			data_z = data_z[np.squeeze(up)]
			data_a = data_a[np.squeeze(up)]
		if fl:
			dn = np.argwhere(data_a[:,0]-data_a[:,1]>=fl)
			data_z = data_z[np.squeeze(dn)]
			data_a = data_a[np.squeeze(dn)]
	else:
		up = np.argwhere(data_z[:,0]<=zh)
		data_z = data_z[np.squeeze(up)]
		data_a = data_a[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]>=zl)
		data_z = data_z[np.squeeze(dn)]
		data_a = data_a[np.squeeze(dn)]
		if fh:
			up = np.argwhere(data_a[:,0]<=fh)
			data_z = data_z[np.squeeze(up)]
			data_a = data_a[np.squeeze(up)]
		if fl:
			dn = np.argwhere(data_a[:,0]>=fl)
			data_z = data_z[np.squeeze(dn)]
			data_a = data_a[np.squeeze(dn)]
	data_z_ = data_z[:,0]
	data_f = data_a[:,0]
	data_f_er = data_z[:,1]
	data_z_er = data_z[:,1]
	return data_f, data_z_, data_f_er, data_z_er


def show_object_details(lens_fol, lens_var, zl, zh=1000, lam_rest=1500., xlim_l=None, xlim_r=None, with_err=None):
	lens_names = [s.split('/')[-1] for s in lens_fol]
	ll = np.argwhere(lens_var==1)
	data_to = []
	if ll.size:
		for l in ll:
			l = l[0]
			filez = glob(lens_fol[l]+'/*_ZPHOT.cat')
			filea = glob(lens_fol[l]+'/*_A.cat*')
			z_pos  = get_var_pos(filez[0], 'zbest')
			f_pos  = get_var_pos(filea[0], 'MAG_'+f_name)
			fr_pos = get_var_pos(filea[0], 'MAGERR_'+f_name)
			data_z = np.loadtxt(filez[0])[:,z_pos:z_pos+2]
			data_m = np.loadtxt(filea[0])
			data_m = np.hstack((np.vstack((data_m[:,f_pos],data_m[:,fr_pos])).T,data_m[:,:5]))
			data = get_object_details(data_z, data_m, zl, zh=zh, fl=xlim_l, fh=xlim_r, with_err=with_err)
			print lens_names[l]
			print 'ID\tRA\tDec\tx\ty\tzb\tzb_err'
			if data.size: 
				for i in xrange(data.shape[0]): 
					print data[i,:]
				data_to.append(lens_names[l])
				data_to.append(data.tolist())
	return data_to

	
def get_object_details(data_z, data_a, zl, zh=100, fl=15, fh=30, with_err=None):
	if with_err:
		up = np.argwhere(data_z[:,0]+data_z[:,1]<=zh)
		data_z = data_z[np.squeeze(up)]
		data_a = data_a[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]-data_z[:,1]>=zl)
		data_z = data_z[np.squeeze(dn)]
		data_a = data_a[np.squeeze(dn)]
		if fh:
			up = np.argwhere(data_a[:,0]+data_a[:,1]<=fh)
			data_z = data_z[np.squeeze(up)]
			data_a = data_a[np.squeeze(up)]
		if fl:
			dn = np.argwhere(data_a[:,0]-data_a[:,1]>=fl)
			data_z = data_z[np.squeeze(dn)]
			data_a = data_a[np.squeeze(dn)]
	else:
		up = np.argwhere(data_z[:,0]<=zh)
		data_z = data_z[np.squeeze(up)]
		data_a = data_a[np.squeeze(up)]
		dn = np.argwhere(data_z[:,0]>=zl)
		data_z = data_z[np.squeeze(dn)]
		data_a = data_a[np.squeeze(dn)]
		if fh:
			up = np.argwhere(data_a[:,0]<=fh)
			data_z = data_z[np.squeeze(up)]
			data_a = data_a[np.squeeze(up)]
		if fl:
			dn = np.argwhere(data_a[:,0]>=fl)
			data_z = data_z[np.squeeze(dn)]
			data_a = data_a[np.squeeze(dn)]
	return np.hstack((data_a[:,2:],data_z))











