import numpy as np
from glob import glob
from Tkinter import *
from find_candidate import *
import matplotlib.pyplot as plt

master = Tk()

data_dir = 'CLASH_data'
lens_fol = glob(data_dir+'/ABELL*')+glob(data_dir+'/MACS*')+glob(data_dir+'/RXJ*')+glob(data_dir+'/MS*')+glob(data_dir+'/CL*')
mags_fol = glob(data_dir+'/high_magnification/*')

lens_names = [s.split('/')[-1] for s in lens_fol]
mags_names = [s.split('/')[-1] for s in mags_fol]

input_lens = np.zeros(20)
input_mags = np.zeros(5)


def search_obj():
	lens = e1.get()
	obj_id = e2.get()
	if lens.upper() not in lens_names+mags_names: print "Enter the correct cluster name."
	elif obj_id == '': print "Enter the object ID."
	else:
		obj_id = float(obj_id)
		if lens.upper() in lens_names: folder = lens_fol[lens_names.index(lens.upper())]
		elif lens.upper() in mags_names: folder = mags_fol[mags_names.index(lens.upper())]
		row = show_object_details_ID(folder, obj_id)
		if row.size:
			print folder.split('/')[-1]
			print row

Label(master, text="Using Object ID:").grid(row=0, column=0, sticky=W)
Label(master, text="Lens Cluster:", fg="green").grid(row=1, column=0)
e1 = Entry(master)
e1.grid(row=1, column=1)
#e1.insert(END, 'all')
Label(master, text="Object ID:", fg="green").grid(row=1, column=2)
e2 = Entry(master)
e2.grid(row=1, column=3)
Button(master, text='Search', command=search_obj).grid(row=1, column=4, pady=4)

mainloop()


