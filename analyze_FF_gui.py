import numpy as np
from glob import glob
from Tkinter import *
from find_candidate_FF import show_hist_z_range#, show_scatter_z, show_object_details
import matplotlib.pyplot as plt

master = Tk()

data_dir = 'FrontierFields_data'
lens_fol = glob(data_dir+'/A2744*')+glob(data_dir+'/M0416*')

lens_names = [s.split('/')[-1] for s in lens_fol]


def print_inputs():
	lens_var, mags_var = get_inputs()
	print e1.get(), e2.get()
	print type(e1.get()), type(e2.get())

def get_inputs():
	lens_var = [0,0,0,0]
	if var00.get(): lens_var[lens_names.index('A2744cl')] = 1
	if var01.get(): lens_var[lens_names.index('A2744PAR')] = 1
	if var10.get(): lens_var[lens_names.index('M0416cl')] = 1
	if var11.get(): lens_var[lens_names.index('M0416PAR')] = 1
	return np.array(lens_var)

def display_hist(save=None):
	lens_var = get_inputs()
	zl, zh = float(e1.get()), float(e2.get())
	bins = float(bn.get())
	plt.clf()
	show_hist_z_range(lens_fol, lens_var, zl, zh=zh, bins=bins)
	if not save: plt.show()

def display_scat(save=None):
	lens_var = get_inputs()
	zl, zh = float(e1.get()), float(e2.get())
	f_name = e4.get()
	if e5.get() == '': xlim_l = None 
	else: xlim_l = float(e5.get())
	if e6.get() == '': xlim_r = None
	else: xlim_r = float(e6.get())
	with_err = werr.get()
	plt.clf()
	show_scatter_z(lens_fol, lens_var, zl, zh=zh, f_name=f_name, xlim_l=xlim_l, xlim_r=xlim_r, with_err=with_err)
	if not save: plt.show()

def display_details():
	lens_var, mags_var = get_inputs()
	camera = np.array([cam_a.get(),cam_i.get()])
	zl, zh = float(e1.get()), float(e2.get())
	stel   = float(e3.get())
	f_name = e4.get()
	if e5.get() == '': xlim_l = None 
	else: xlim_l = float(e5.get())
	if e6.get() == '': xlim_r = None
	else: xlim_r = float(e6.get())
	with_err = werr.get()
	data = show_object_details(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=zh, stel=stel, f_name=f_name, xlim_l=xlim_l, xlim_r=xlim_r, with_err=with_err)
	return data

def clear_figure():
	plt.clf()
	plt.show()

def write_to_file():
	filename = e7.get()
	data = display_details()
	fname = 'output/'+filename+'_info.txt'
	print "Data saved as", fname
	ff = open(fname, 'w')
	header = 'ID\tRA\tDec\tx\ty\tzb\tzbmin\tzbmax\n'
	for i in xrange(len(data)):
		if i%2==0:
			ff.writelines(data[i]+'\n')
		else:
			ff.writelines(header)
			dat = [str(d) for d in data[i]]	
			for da in dat:
				ff.writelines(da)
				ff.writelines('\n')
	ff.close()

def save_scatter():
	filename = e7.get()
	fname = 'output/'+filename+'_scatter.png'
	display_scat(save=True)
	print "The figure is saved as", fname
	plt.savefig(fname)

def save_histogram():
	filename = e7.get()
	fname = 'output/'+filename+'_histogram.png'
	display_hist(save=True)
	print "The figure is saved as", fname
	plt.savefig(fname)

Label(master, text="Frontier Fields Clusters:", fg="green").grid(row=0, sticky=W)
Label(master, text="ABELL2744").grid(row=1, column=0)
var00 = IntVar()
Checkbutton(master, text='cluster', variable=var00).grid(row=1, column=1,sticky=W)
var01 = IntVar()
Checkbutton(master, text='parallel', variable=var01).grid(row=1, column=2,sticky=W)
Label(master, text="MACS0416").grid(row=2, column=0)
var10 = IntVar()
Checkbutton(master, text='cluster', variable=var10).grid(row=2, column=1,sticky=W)
var11 = IntVar()
Checkbutton(master, text='parallel', variable=var11).grid(row=2, column=2,sticky=W)

Label(master, text="Redshift range:", fg="red").grid(row=9, sticky=W)

Label(master, text="z range:").grid(row=10, column=0)
#Label(master, text="upper z").grid(row=11, column=2)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=10, column=1)
e2.grid(row=10, column=2)
e1.insert(END, '6')
e2.insert(END, '100')
werr = IntVar()
Checkbutton(master, text='with errorbar', variable=werr).grid(row=10, column=3,sticky=W)

Label(master, text="No. of z bins").grid(row=11, column=0)
bn = Entry(master)
bn.grid(row=11, column=1)
bn.insert(END, '10')

Label(master, text="Filter name:", fg="red").grid(row=12, column=0, sticky=W)
e4 = Entry(master)
e4.grid(row=12, column=1)
e4.insert(END, 'Y105')

Label(master, text="Magnitude range:").grid(row=13, column=0)
e5 = Entry(master)
e5.grid(row=13, column=1)
e6 = Entry(master)
e6.grid(row=13, column=2)

Label(master, text="Enter filename:").grid(row=15, column=0)
e7 = Entry(master)
e7.grid(row=15, column=1)
e7.insert(END, 'test')

#file_app = IntVar(value=1)
#Checkbutton(master, text='Append data', variable=file_app).grid(row=15, column=2,sticky=W)

Button(master, text='Histogram', command=display_hist).grid(row=14, column=0, pady=4)
Button(master, text='Scatter', command=display_scat).grid(row=14, column=1, pady=4)
Button(master, text='Get details', command=display_details).grid(row=14, column=2, pady=4)
Button(master, text='Clear', command=clear_figure).grid(row=14, column=3, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=14, column=4, pady=4)
Button(master, text='Write to File', command=write_to_file).grid(row=15, column=2, pady=4)
Button(master, text='Save scatter-plot', command=save_scatter).grid(row=15, column=3, pady=4)
Button(master, text='Save histogram', command=save_histogram).grid(row=15, column=4, pady=4)
mainloop()
