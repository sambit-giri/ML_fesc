import numpy as np
from glob import glob
from Tkinter import *
from find_candidate import show_hist_z_range
import matplotlib.pyplot as plt

master = Tk()

data_dir = '/disk/dawn-1/sgiri/ML_project/ML_fesc/CLASH_data'
lens_fol = glob(data_dir+'/ABELL*')+glob(data_dir+'/MACS*')+glob(data_dir+'/RXJ*')+glob(data_dir+'/MS*')+glob(data_dir+'/CL*')
mags_fol = glob(data_dir+'/high_magnification/*')

lens_names = [s.split('/')[-1] for s in lens_fol]
mags_names = [s.split('/')[-1] for s in mags_fol]

input_lens = np.zeros(20)
input_mags = np.zeros(5)

def var_states():
   print("X-ray clusters: %d,\nHigh magnification clusters: %d" % (var1.get()+var2.get(), var3.get()+var4.get()))

def print_inputs():
	lens_var, mags_var = get_inputs()
	print e1.get(), e2.get()
	print type(e1.get()), type(e2.get())

def get_inputs():
	lens_var = [var00.get(),var01.get(),var02.get(),var03.get(),var04.get(),var05.get(),var06.get(),var07.get(),var08.get(),var09.get(),var10.get(),var11.get(),var12.get(),var13.get(),var14.get(),var15.get(),var16.get(),var17.get(),var18.get(),var19.get()]
	mags_var = [var20.get(),var21.get(),var22.get(),var23.get(),var24.get()]
	return np.array(lens_var), np.array(mags_var)

def display_hist():
	lens_var, mags_var = get_inputs()
	camera = np.array([cam_a.get(),cam_i.get()])
	zl, zh = float(e1.get()), float(e2.get())
	stel   = float(e3.get())
	#print lens_var, mags_var
	#print camera
	#print zl, zh
	plt.clf()
	show_hist_z_range(lens_fol, mags_fol, lens_var, mags_var, camera, zl, zh=zh, bins=10, stel=stel)
	plt.show()

def clear_figure():
	plt.clf()
	plt.show()

Label(master, text="X-ray Selected Clusters:").grid(row=0, sticky=W)

var00 = IntVar()
Checkbutton(master, text=lens_names[0], variable=var00).grid(row=1, column=0,sticky=W)
var01 = IntVar()
Checkbutton(master, text=lens_names[1], variable=var01).grid(row=1, column=1,sticky=W)
var02 = IntVar()
Checkbutton(master, text=lens_names[2], variable=var02).grid(row=1, column=2,sticky=W)
var03 = IntVar()
Checkbutton(master, text=lens_names[3], variable=var03).grid(row=1, column=3,sticky=W)
var04 = IntVar()
Checkbutton(master, text=lens_names[4], variable=var04).grid(row=1, column=4,sticky=W)
var05 = IntVar()
Checkbutton(master, text=lens_names[5], variable=var05).grid(row=2, column=0,sticky=W)
var06 = IntVar()
Checkbutton(master, text=lens_names[6], variable=var06).grid(row=2, column=1,sticky=W)
var07 = IntVar()
Checkbutton(master, text=lens_names[7], variable=var07).grid(row=2, column=2,sticky=W)
var08 = IntVar()
Checkbutton(master, text=lens_names[8], variable=var08).grid(row=2, column=3,sticky=W)
var09 = IntVar()
Checkbutton(master, text=lens_names[9], variable=var09).grid(row=2, column=4,sticky=W)
var10 = IntVar()
Checkbutton(master, text=lens_names[10], variable=var10).grid(row=3, column=0,sticky=W)
var11 = IntVar()
Checkbutton(master, text=lens_names[11], variable=var11).grid(row=3, column=1,sticky=W)
var12 = IntVar()
Checkbutton(master, text=lens_names[12], variable=var12).grid(row=3, column=2,sticky=W)
var13 = IntVar()
Checkbutton(master, text=lens_names[13], variable=var13).grid(row=3, column=3,sticky=W)
var14 = IntVar()
Checkbutton(master, text=lens_names[14], variable=var14).grid(row=3, column=4,sticky=W)
var15 = IntVar()
Checkbutton(master, text=lens_names[15], variable=var15).grid(row=4, column=0,sticky=W)
var16 = IntVar()
Checkbutton(master, text=lens_names[16], variable=var16).grid(row=4, column=1,sticky=W)
var17 = IntVar()
Checkbutton(master, text=lens_names[17], variable=var17).grid(row=4, column=2,sticky=W)
var18 = IntVar()
Checkbutton(master, text=lens_names[18], variable=var18).grid(row=4, column=3,sticky=W)
var19 = IntVar()
Checkbutton(master, text=lens_names[19], variable=var19).grid(row=4, column=4,sticky=W)

Label(master, text="High Magnification Clusters:").grid(row=5, sticky=W)
var20 = IntVar()
Checkbutton(master, text=mags_names[0], variable=var20).grid(row=6, column=0,sticky=W)
var21 = IntVar()
Checkbutton(master, text=mags_names[1], variable=var21).grid(row=6, column=1,sticky=W)
var22 = IntVar()
Checkbutton(master, text=mags_names[2], variable=var22).grid(row=6, column=2,sticky=W)
var23 = IntVar()
Checkbutton(master, text=mags_names[3], variable=var23).grid(row=6, column=3,sticky=W)
var24 = IntVar()
Checkbutton(master, text=mags_names[4], variable=var24).grid(row=6, column=4,sticky=W)

Label(master, text="Camera:").grid(row=7, sticky=W)
cam_a = IntVar(value=1)
Checkbutton(master, text='ACS+IR', variable=cam_a).grid(row=8, column=0,sticky=W)
cam_i = IntVar(value=1)
Checkbutton(master, text='IR', variable=cam_i).grid(row=8, column=1,sticky=W)

Label(master, text="Redshift range:").grid(row=9, sticky=W)

Label(master, text="lower z").grid(row=10, column=0)
Label(master, text="upper z").grid(row=10, column=2)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=10, column=1)
e2.grid(row=10, column=3)
e1.insert(END, '6')
e2.insert(END, '1000')

Label(master, text="Stel threshold:").grid(row=11, column=0, sticky=W)
e3 = Entry(master)
e3.grid(row=11, column=1)
e3.insert(END, '0.2')

Button(master, text='Histogram', command=display_hist).grid(row=12, column=0, sticky=W, pady=4)
Button(master, text='Clear', command=clear_figure).grid(row=12, column=1, sticky=W, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=12, column=2, sticky=W, pady=4)
mainloop()
