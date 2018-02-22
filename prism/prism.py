##-------------------------------------------------------------
#    ____  ____  ___ ____  __  __     
#   |  _ \|  _ \|_ _/ ___||  \/  |  _ 
#   | |_) | |_) || |\___ \| |\/| | (_)
#   |  __/|  _ < | | ___) | |  | |  _ 
#   |_|   |_| \_\___|____/|_|  |_| (_)
#                                     
#   ___                 _      _                  __                   __      
#    | _  _ ||_  _ \/ _|__ ._ |_).__ |_  _.|_ o|o(__|_o _  /\  _ _    (__|_o _ 
#    |(_)(_)||_)(_)/\  |(_)|  |  |(_)|_)(_||_)|||__)|_|(_ /--\(_(_)|_|__)|_|(_ 
#                                                                              
#    __                                          
#   (_  _  _|o._ _  _ .__|_ |\/| _.._ ._ o._  _  
#   __)(/_(_||| | |(/_| ||_ |  |(_||_)|_)|| |(_| 
#                                  |  |       _| 
#
#   |b|y| |D|a|n|i|e|l| |B|u|s|c|o|m|b|e|
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |d|a|n|i|e|l|.|b|u|s|c|o|m|b|e|@|n|a|u|.|e|d|u|


# general
from __future__ import division
import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(divide='ignore')
np.seterr(invalid='ignore')
import os

# gui
if sys.version[0]=='3':
   import tkinter as Tkinter
   from tkinter.tix import *
   from tkinter import ttk
   from tkinter.scrolledtext import ScrolledText
   from tkinter.filedialog import askopenfilename
   from tkinter import messagebox as tkMessageBox
else:
   import Tkinter
   from Tix import *
   import ttk
   from ScrolledText import ScrolledText
   from tkFileDialog import askopenfilename
   import tkMessageBox

from tkcolorpicker import askcolor
from PIL import Image, ImageTk

# prism functions
from common_funcs import get_sparse_labels
from gmm_funcs import fit_GMM, apply_GMM
from crf_funcs import apply_CRF
from read_funcs import *
from plot_funcs import *
from write_funcs import *
from eval_funcs import *
##-------------------------------------------------------------

##-------------------------------------------------------------
def gui():

	#=======================
	# NOTE: Frame will make a top-level window if one doesn't already exist which
	# can then be accessed via the frame's master attribute
	# make a Frame whose parent is root, named "prism"
	master = Tkinter.Frame(name='prism')

	self = master.master  # short-cut to top-level window
	master.pack()  # pack the Frame into root, defaults to side=TOP
	self.title('PriSM: Probabilistic Acoustic Sediment Mapping')  # name the window

	# field for DAT filename
	self.DATfilename = Tkinter.StringVar()
	self.DATfilename.set(u" ")

	# field for bed filename
	self.BEDfilename = Tkinter.StringVar()
	self.BEDfilename.set(None)
	       
	# create notebook
	demoPanel = Tkinter.Frame(master, name='demo')  # create a new frame slaved to master
	demoPanel.pack()  # pack the Frame into root

	# create (notebook) demo panel
	nb = ttk.Notebook(demoPanel, name='notebook')  # create the ttk.Notebook widget

	# extend bindings to top level window allowing
	#   CTRL+TAB - cycles thru tabs
	#   SHIFT+CTRL+TAB - previous tab
	#   ALT+K - select tab using mnemonic (K = underlined letter)
	nb.enable_traversal()

	nb.pack(fill=Tkinter.BOTH, expand=Tkinter.Y, padx=2, pady=3)  # add margin

	#==============================================================
	#==============================================================
	#========START about tab

	# create description tab
	# frame to hold (tab) content
	frame = Tkinter.Frame(nb, name='descrip')

	frame.configure(background='black')

	# widgets to be displayed on 'Description' tab
	About_msg = [
	    "PriSM is a program for substrate mapping using multibeam acoustic backscatter",
	    "using a task-specific probabilistic approach\n",
	    "\n",
	    "It works with both single-frequency (monospectral) and\n",
	    "multi-frequency (multispectral) backscatter data inputs\n",
	    "\n",
	    "Two models are implemented:\n",
	    "1) Gaussian Mixture Model (GMM) and 2) fully-connected Conditional Random Field (CRF)\n",
	    "\n",
	    "The program is written and maintained by Dr Daniel Buscombe,\n",
	    "Northern Arizona University. Email daniel.buscombe@nau.edu\n",
	    "\n",    
	    "The tabs are to be navigated in order (read, classify, plot, export)\n",
	    "\n",
	    "Please visit the website for more info: https://www.danielbuscombe.com/prism/"]

	lbl = Tkinter.Label(frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(About_msg), fg="white")
	lbl.configure(background='black')
		        
	# position and set resize behavior
	lbl.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
	frame.rowconfigure(1, weight=1)
	frame.columnconfigure((0,1), weight=1, uniform=1)

	# make panel for logo
	image_panel = Tkinter.Canvas(frame, width = 250, height =232)#, cursor = "cross")
	image_panel.grid(column = 0, row = 2)
	image_panel.configure(background='black')
	 
	#show_image = ImageTk.PhotoImage(Image.open(prism.__path__[0]+os.sep+"prism_logo_blk.png"))
	show_image = ImageTk.PhotoImage(Image.open(".."+os.sep+"prism_logo_blk_sm.png"))
	# show the panel
	image_panel.create_image(0, 0, anchor=Tkinter.NW, image=show_image) 
		
	# add to notebook (underline = index for short-cut character)
	nb.add(frame, text='About', underline=0, padding=2)

	#==============================================================
	#==============================================================
	#========END about tab


	#==============================================================
	#==============================================================
	#========START read tab

	# Populate the second pane. Note that the content doesn't really matter
	read_frame = Tkinter.Frame(nb)
	nb.add(read_frame, text='Read Data')#, state='disabled')

	read_frame.configure(background='#ff7b25')

	Read_msg = [
	    "INSTRUCTIONS:\n\n",
	    "1. Select backscatter geotiff file(s) \n\n",
	    "2. Select bed observations file (csv or ESRI shapefile)\n\n",
	    "3. Set output grid resolution (m). Default=1\n\n" ,  
	    "4. Set buffer distance (m). Default=10\n\n",    
	    "5. Set weight for chambolle filter (0 for no filter). Default=0.2"]

	lbl2 = Tkinter.Label(read_frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(Read_msg))

	lbl2.configure(background='#6b5b95', fg="white")
		        
	# position and set resize behavior
	lbl2.grid(row=0, column=0, columnspan=1, sticky='new', pady=5)

	#=======================
	# get backscatter data file(s)         
	datVar = Tkinter.StringVar()
	self.read_bs_btn = Tkinter.Button(read_frame, text='Get backscatter data file(s)', underline=0,
		         command=lambda v=datVar: _get_DAT(master, v))
	dat = Tkinter.Label(read_frame, textvariable=datVar, name='dat')
	self.read_bs_btn.grid(row=1, column=0, pady=(2,4))
	self.read_bs_btn.configure(background='#6b5b95', fg="white")

	#=======================
	# get bed observation file
	bedVar = Tkinter.StringVar()
	self.read_bed_btn = Tkinter.Button(read_frame, text='Get bed observations file', underline=0,
		         command=lambda v=bedVar: _get_BED(master, v))
	bed = Tkinter.Label(read_frame, textvariable=bedVar, name='dat')
	self.read_bed_btn.grid(row=1, column=1, pady=(2,4))
	self.read_bed_btn.configure(background='#6b5b95', fg="white")

	#=======================
	# grid res
	self.gridvar = Tkinter.DoubleVar()
	gscale = Tkinter.Scale( read_frame, variable = self.gridvar, from_=1, to=20, resolution=1, tickinterval=2, label = 'Grid Resolution [m]' )
	gscale.set(1)
	gscale.grid(row=2, column=0,  pady=(2,4))
	gscale.configure(background='#6b5b95', fg="white")

	#=======================
	# buff
	self.buffvar = Tkinter.DoubleVar()
	bscale = Tkinter.Scale( read_frame, variable = self.buffvar, from_=1, to=30, resolution=1, tickinterval=5, label = 'Buffer distance [m]' )
	bscale.set(10)
	bscale.grid(row=2, column=1,  pady=(2,4))
	bscale.configure(background='#6b5b95', fg="white")

	#=======================
	# chambolle
	self.cvar = Tkinter.DoubleVar()
	cscale = Tkinter.Scale( read_frame, variable = self.cvar, from_=0, to=1, resolution=.1, tickinterval=.1, label = 'Chambolle weight [non-dim.]' )
	cscale.set(0.2)
	cscale.grid(row=3, column=0,  pady=(2,4))
	cscale.configure(background='#6b5b95', fg="white")

	#=======================
	# process button
	self.proc_btn = Tkinter.Button(read_frame, text='Go!', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _proc(self))
	self.proc_btn.grid(row=3, column=1, pady=(2,4))
	self.proc_btn.configure(background='#6b5b95', fg="white")


	#==============================================================
	#========START functions for read tab

	#=======================
	def _proc(self):
           """
           this function ...
           """
           infiles = self.DATfilename.get().split() 
           input = []
           for k in infiles:
              k = k.replace(',','')
              k = k.replace('(','')
              k = k.replace(')','')
              k = k.replace("'",'')
              input.append(k)
              print('Backscatter file: %s' % k)

           print('Grid size: %i m' % self.gridvar.get())
           print('Chambolle weight: %f' % self.cvar.get())

           self.img, self.bs = read_geotiff(input, self.gridvar.get(), self.cvar.get())

           print('Bed observations file: %s' % self.BEDfilename.get())
           print('Buffer size: %i m' % self.buffvar.get())

           name, ext = os.path.splitext(self.BEDfilename.get())
           if ext == '.shp':
              self.bed = read_shpfile(self.BEDfilename.get(), self.bs)
           elif ext == '.csv':
              self.bed = read_csvfile(self.BEDfilename.get(), self.bs)
           elif ext == '.txt':
              self.bed = read_csvfile(self.BEDfilename.get(), self.bs)
           else:
              tkMessageBox.showinfo("Error", "Bed Observation file format not supported") 

           if hasattr(self, 'bed'): 

              self.Lc = get_sparse_labels(self.bs, self.bed, np.int(self.buffvar.get()) )
			  
              if np.ndim(self.img)>2:
                 self.mask = self.img[:,:,0]==0
              else:
                 self.mask = self.img==0
              
              self.proc_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Read module finished") 
           else:
              tkMessageBox.showinfo("Error", "Select valid bed observation file first!") 


	#=======================        
	def _get_DAT(master, v):
           """
           this function ...
           """
           self.DATfile = askopenfilename(filetypes=[("Backscatter data files","*.tif *.tiff *.TIF *.TIFF")], multiple=True)

           self.DATfilename.set(self.DATfile)
	    
           self.read_bs_btn.configure(fg='#d64161', background="white")

           self.update()    

	#=======================
	def _get_BED(master, v):
           """
           this function ...
           """
           self.bedfile = askopenfilename(filetypes=[("Bed data files","*.shp *.csv")], multiple=False)

           self.BEDfilename.set(self.bedfile)

           self.read_bed_btn.configure(fg='#d64161', background="white")
  
           self.update()    
       
	#==============================================================
	#========END functions for read tab

	#==============================================================
	#==============================================================
	#========END read tab


	#==============================================================
	#==============================================================
	#========START classify GMM tab

	# Populate the second pane. Note that the content doesn't really matter
	class1_frame = Tkinter.Frame(nb)
	nb.add(class1_frame, text='Classify: GMM')#, state='disabled')

	class1_frame.configure(background='#fff2df')

	Read_msg = [
	    "INSTRUCTIONS:\n\n",
	    "1. Select proportion of data to use for test. Default=0.5 \n\n",
	    "2. Set probability threshold (probabilities less than this are 'unknown'). Default=0.7\n\n",
	    "3. Select covariance type. Default=1\n",
	    "   1='full' (each component has its own general covariance matrix)\n" ,  
	    "   2='tied' (all components share the same general covariance matrix)\n" ,  
	    "   3='diagonal' (each component has its own diagonal covariance matrix)\n" ,  
	    "   4='spherical' (each component has its own single variance)\n\n" ,  
	    "4. Set tolerance. Default=1e-2"]


	lbl2 = Tkinter.Label(class1_frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(Read_msg))

	lbl2.configure(background='#674d3c', fg="white")
		        
	# position and set resize behavior
	lbl2.grid(row=0, column=0, columnspan=1, sticky='new', pady=5)

	#=======================
	# prob thres
	self.pvar = Tkinter.DoubleVar()
	pscale = Tkinter.Scale( class1_frame, variable = self.pvar, from_=0.1, to=.9, resolution=.1, tickinterval=.2, label = 'Prob. threshold' )
	pscale.set(0.7)
	pscale.grid(row=0, column=1,  pady=(2,4))
	pscale.configure(background='#674d3c', fg="white")

	#=======================
	# test size
	self.tvar = Tkinter.DoubleVar()
	tscale = Tkinter.Scale( class1_frame, variable = self.tvar, from_=0.1, to=.9, resolution=.1, tickinterval=.2, label = 'Test proportion' )
	tscale.set(0.5)
	tscale.grid(row=2, column=0,  pady=(2,4))
	tscale.configure(background='#674d3c', fg="white")

	#=======================
	# covariance
	self.covvar = Tkinter.DoubleVar()
	covscale = Tkinter.Scale( class1_frame, variable = self.covvar, from_=1, to=4, resolution=1, tickinterval=1, label = 'Covariance type' )
	covscale.set(1)
	covscale.grid(row=2, column=1,  pady=(2,4))
	covscale.configure(background='#674d3c', fg="white")

	#=======================
	# tolerance
	self.tolvar = Tkinter.DoubleVar()
	tolscale = Tkinter.Scale( class1_frame, variable = self.tolvar, from_=1e-4, to=1e-1, resolution=1e-4, tickinterval=1e-4, label = 'Tolerance' )
	tolscale.set(1e-2)
	tolscale.grid(row=3, column=0,  pady=(2,4))
	tolscale.configure(background='#674d3c', fg="white")

	#=======================
	# process button
	self.gmmproc_btn = Tkinter.Button(class1_frame, text='Go!', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _procGMM(self))
	self.gmmproc_btn.grid(row=3, column=1, pady=(2,4))
	self.gmmproc_btn.configure(background='#674d3c', fg="white")


	#==============================================================
	#========START functions for classify GMM tab

	#=======================
	def _procGMM(self):
           """
           this function ...
           """
           if self.covvar.get()==1:
              cov = 'full'
           if self.covvar.get()==2:
              cov = 'tied'
           if self.covvar.get()==3:
              cov = 'diag'
           if self.covvar.get()==4:
              cov = 'spherical'

           print('Prob. threshold: %g' % self.pvar.get())
           print('Covariance: %s' % cov)
           print('Tolerance: %f' % self.tolvar.get())
           print('Test size: %f' % self.tvar.get())

           if hasattr(self, 'img'): 
              self.g = fit_GMM(self.img, self.Lc, self.tvar.get(), cov, self.tolvar.get())

              self.y_pred_gmm, self.y_prob_gmm, self.y_prob_per_class_gmm = apply_GMM(self.g, self.img, self.pvar.get())

              self.gmmproc_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "GMM:Classify module finished")
 
           else:
              tkMessageBox.showinfo("Error", "Read backscatter data in first!") 


	#==============================================================
	#========END functions for classify GMM tab

	#==============================================================
	#==============================================================
	#========END classify GMM tab


	#==============================================================
	#==============================================================
	#========START classify CRF tab

	# Populate the second pane. Note that the content doesn't really matter
	class2_frame = Tkinter.Frame(nb)
	nb.add(class2_frame, text='Classify: CRF')#, state='disabled')

	class2_frame.configure(background='#FFBB00')

	Read_msg = [
	    "INSTRUCTIONS:\n\n",
	    "1. Set probability threshold (probabilities less than this are 'unknown'). Default=0.7\n\n",
	    "2. Set number of iterations. Default=15 \n\n",
	    "3. Set similarity parameter, theta: controls the degree of allowable similarity in backscatter between graph nodes. Default=300 \n\n",
	    "4. Set proximity tolerance, mu: specifies the max. distance between pairs of pixels that can have similar backscatter but different substrate labels. Default=100"]


	lbl2 = Tkinter.Label(class2_frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(Read_msg))

	lbl2.configure(background='#4040a1', fg="white")
		        
	# position and set resize behavior
	lbl2.grid(row=0, column=0, columnspan=1, sticky='new', pady=5)

	#=======================
	# prob thres
	self.pvar = Tkinter.DoubleVar()
	pscale = Tkinter.Scale( class2_frame, variable = self.pvar, from_=0.1, to=.9, resolution=.1, tickinterval=.2, label = 'Prob. threshold' )
	pscale.set(0.7)
	pscale.grid(row=0, column=1,  pady=(2,4))
	pscale.configure(background='#4040a1', fg="white")

	#=======================
	# iterations
	self.nvar = Tkinter.DoubleVar()
	nscale = Tkinter.Scale( class2_frame, variable = self.nvar, from_=1, to=30, resolution=1, tickinterval=5, label = 'Number of iterations' )
	nscale.set(15)
	nscale.grid(row=2, column=0,  pady=(2,4))
	nscale.configure(background='#4040a1', fg="white")

	#=======================
	# theta
	self.thetavar = Tkinter.DoubleVar()
	thetascale = Tkinter.Scale( class2_frame, variable = self.thetavar, from_=10, to=1000, resolution=10, tickinterval=100, label = 'Theta' )
	thetascale.set(300)
	thetascale.grid(row=2, column=1,  pady=(2,4))
	thetascale.configure(background='#4040a1', fg="white")

	#=======================
	# mu
	self.muvar = Tkinter.DoubleVar()
	muscale = Tkinter.Scale( class2_frame, variable = self.muvar, from_=10, to=600, resolution=10, tickinterval=100, label = 'Mu' )
	muscale.set(100)
	muscale.grid(row=3, column=0,  pady=(2,4))
	muscale.configure(background='#4040a1', fg="white")

	#=======================
	# process button
	self.crfproc_btn = Tkinter.Button(class2_frame, text='Go!', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _procCRF(self))
	self.crfproc_btn.grid(row=3, column=1, pady=(2,4))
	self.crfproc_btn.configure(background='#4040a1', fg="white")


	#==============================================================
	#========START functions for CRF classify tab

	#=======================
	def _procCRF(self):
           """
           this function ...
           """
           print('Iterations: %g' % self.nvar.get())
           print('Prob. threshold: %g' % self.pvar.get())
           print('Theta: %f' % self.thetavar.get())
           print('Mu: %f' % self.muvar.get())

           if hasattr(self, 'img'): 
              self.y_pred_crf, self.y_prob_crf, self.y_prob_per_class_crf = apply_CRF(self.img, self.Lc, self.bed['labels'], np.int(self.nvar.get()), self.pvar.get(), np.int(self.thetavar.get()), np.int(self.muvar.get()) )

              self.crfproc_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "CRF:Classify module finished") 
 
           else:
              tkMessageBox.showinfo("Error", "Read backscatter data in first!") 


	#==============================================================
	#========END functions for classify CRF tab

	#==============================================================
	#==============================================================
	#========END classify CRF tab


	#==============================================================
	#==============================================================
	#========START plot tab

	# Populate the second pane. Note that the content doesn't really matter
	plot_frame = Tkinter.Frame(nb)
	nb.add(plot_frame, text='Plot')#, state='disabled')

	plot_frame.configure(background='#d5e1df')

	Read_msg = [
	    "INSTRUCTIONS:\n\n",
	    "1. Write a prefix for file names and press Enter\n"
	    "2. Make a color ramp by selecting colors for each substrate\n"
	    "3. Press buttons to make plots!\n"
	    "   GMM map = GMM predicted substrate & prob. maps\n" ,  
	    "   CRF map = CRF predicted substrate & prob. maps\n" ,  
	    "   *GMM map + image = GMM predicted substrate & prob. maps with background image\n" ,  
	    "   *CRF map + image = CRF predicted substrate & prob. maps with background image\n" , 
	    "   GMM & CRF maps = GMM and CRF predicted substrate maps side by side\n" ,    
	    "   *GMM & CRF maps + image = GMM and CRF predicted substrate maps side by side with background images\n" ,    
	    "   Backscatter per substrate = histograms of backscatter per substrate type\n" ,  
	    "   Backscatter maps = maps backscatter with and without background image\n" ,  
            "* = requires internet connection"
             ]


	lbl2 = Tkinter.Label(plot_frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(Read_msg))

	lbl2.configure(background='#405d27', fg="white")
		        
	# position and set resize behavior
	lbl2.grid(row=0, column=0, columnspan=1, sticky='new', pady=5)


	#=======================
	# check button for prefix
	self.prefix = Tkinter.StringVar()
	self.prefix_entry = Tkinter.Entry(plot_frame, width = 30, textvariable = self.prefix)
	self.prefix_entry.grid(row=1, column=0, pady=(2,4))
	self.prefix_entry.bind("<Return>", lambda epsg=self.prefix.get(): _OnPressEnter1(self))
	self.prefix.set(u"Site Name")
	self.prefix_entry.configure(background='#405d27', fg="white")

	#=======================
	# check button for cmap
	self.cmap_btn = Tkinter.Button(plot_frame, text='Pick color ramp', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _pick_cmap(self))
	self.cmap_btn.grid(row=1, column=1, pady=(2,4))
	self.cmap_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 1 
	self.plot1_btn = Tkinter.Button(plot_frame, text='GMM map', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_gmm(self))
	self.plot1_btn.grid(row=2, column=0, pady=(2,4))
	self.plot1_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 2 
	self.plot2_btn = Tkinter.Button(plot_frame, text='CRF map', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_crf(self))
	self.plot2_btn.grid(row=2, column=1, pady=(2,4))
	self.plot2_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 3 
	self.plot3_btn = Tkinter.Button(plot_frame, text='GMM map + base image', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_gmm_image(self))
	self.plot3_btn.grid(row=3, column=0, pady=(2,4))
	self.plot3_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 4 
	self.plot4_btn = Tkinter.Button(plot_frame, text='CRF map + base image', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_crf_image(self))
	self.plot4_btn.grid(row=3, column=1, pady=(2,4))
	self.plot4_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 2a 
	self.plot2a_btn = Tkinter.Button(plot_frame, text='CRF & GMM maps', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_gmm_crf(self))
	self.plot2a_btn.grid(row=4, column=0, pady=(2,4))
	self.plot2a_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 4a 
	self.plot4a_btn = Tkinter.Button(plot_frame, text='CRF & GMM maps + image', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_gmm_crf_images(self))
	self.plot4a_btn.grid(row=4, column=1, pady=(2,4))
	self.plot4a_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 5
	self.plot5_btn = Tkinter.Button(plot_frame, text='Backscatter per substrate', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_dists_per_sed(self))
	self.plot5_btn.grid(row=5, column=0, pady=(2,4))
	self.plot5_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 6
	self.plot6_btn = Tkinter.Button(plot_frame, text='Backscatter maps', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_bs(self))
	self.plot6_btn.grid(row=5, column=1, pady=(2,4))
	self.plot6_btn.configure(background='#405d27', fg="white")

	#=======================
	# check button for plot 7
	self.plot7_btn = Tkinter.Button(plot_frame, text='GMM confusion matrix', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_cm_gmm(self))
	self.plot7_btn.grid(row=6, column=0, pady=(2,4))
	self.plot7_btn.configure(background='#405d27', fg="white")


	#=======================
	# check button for plot 8
	self.plot8_btn = Tkinter.Button(plot_frame, text='CRF confusion matrix', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _plot_cm_crf(self))
	self.plot8_btn.grid(row=6, column=1, pady=(2,4))
	self.plot8_btn.configure(background='#405d27', fg="white")


	#==============================================================
	#========START functions for plot tab

	#=======================
	# must press enter to set 
	def _OnPressEnter1(self):
           """
           sets prefix for file names on Enter press
           """
           self.prefix.set( self.prefix.get() )
           self.prefix_entry.focus_set()
           self.prefix_entry.selection_range(0, Tkinter.END)
           print('file name prefix set to %s ' % (str(self.prefix.get())))
           self.update()

	#=======================
	def _pick_cmap(self):
           """
           this function ...
           """
           labs = self.bed['labels'] #['1', '2', '3', '4'] #

           cmap = []
           for lab in labs:
              root = Tkinter.Tk()
              style = ttk.Style(root)
              style.theme_use('clam')

              rgb, html = askcolor((255, 255, 0), root, title='Pick color for substrate: '+lab)
              root.destroy()
              cmap.append(html)

           self.cmap = cmap
           self.cmap_btn.configure(fg='#d64161', background="white")
           self.update()

	#=======================
	def _plot_gmm(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'): 

              in1 = self.y_pred_gmm.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_gmm.copy()
              #in2[self.mask] = np.nan

              plot_gmm(self.mask, in1, in2, self.bs, 
                       self.bed, self.cmap, self.prefix.get())

              self.plot1_btn.configure(fg='#d64161', background="white")

              del in1, in2
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 


	#=======================
	def _plot_crf(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'):

              in1 = self.y_pred_crf.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_crf.copy()
              #in2[self.mask] = np.nan

              plot_crf(self.mask, in1, in2, self.bs, 
                       self.bed, self.cmap, self.prefix.get())

              self.plot2_btn.configure(fg='#d64161', background="white")

              del in1, in2
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 


	#=======================
	def _plot_gmm_image(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'):

              in1 = self.y_pred_gmm.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_gmm.copy()
              #in2[self.mask] = np.nan

              plot_gmm_image(self.mask, in1, in2, self.bs, 
                             self.bed, self.cmap, self.prefix.get())

              self.plot3_btn.configure(fg='#d64161', background="white")

              del in1, in2
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 

	#=======================
	def _plot_crf_image(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'):
              in1 = self.y_pred_crf.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_crf.copy()
              #in2[self.mask] = np.nan

              plot_crf_image(self.mask, in1, in2, self.bs, 
                             self.bed, self.cmap, self.prefix.get())

              self.plot4_btn.configure(fg='#d64161', background="white")

              del in1, in2
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 

	#=======================
	def _plot_gmm_crf(self):
           """
           this function ...
           """
           if hasattr(self, 'y_pred_gmm') and hasattr(self, 'y_pred_crf'):

              in1 = self.y_pred_gmm.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_gmm.copy()
              #in2[self.mask] = np.nan

              in3 = self.y_pred_crf.copy()
              #in3[self.mask] = np.nan

              in4 = self.y_prob_crf.copy()
              #in4[self.mask] = np.nan

              plot_gmm_crf(self.mask, in1, in2, in3, in4, self.bs, self.bed, self.cmap, self.prefix.get())

              self.plot2a_btn.configure(fg='#d64161', background="white")

              del in1, in2, in3, in4
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Process", "Process both GMM and CRF first!") 

	#=======================
	def _plot_gmm_crf_images(self):
           """
           this function ...
           """
           if hasattr(self, 'y_pred_gmm') and hasattr(self, 'y_pred_crf'):

              in1 = self.y_pred_gmm.copy()
              #in1[self.mask] = np.nan

              in2 = self.y_prob_gmm.copy()
              #in2[self.mask] = np.nan

              in3 = self.y_pred_crf.copy()
              #in3[self.mask] = np.nan

              in4 = self.y_prob_crf.copy()
              #in4[self.mask] = np.nan

              plot_gmm_crf_images(self.mask, in1, in2, in3, in4, self.bs, self.bed, self.cmap, self.prefix.get())

              self.plot4a_btn.configure(fg='#d64161', background="white")

              del in1, in2, in3, in4
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Process", "Process both GMM and CRF first!") 

	#=======================
	def _plot_dists_per_sed(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'):
              plot_dists_per_sed(self.Lc.copy(), self.img, self.bed, self.cmap, self.prefix.get())

              self.plot5_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 

	#=======================
	def _plot_bs(self):
           """
           this function ...
           """
           if hasattr(self, 'cmap'):
              plot_bs_maps(self.img, self.bed, self.bs, self.cmap, self.prefix.get())

              self.plot6_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Pick colors", "Pick color ramp first!") 

	#=======================
	def _plot_cm_gmm(self):
           """
           this function ...
           """
           if hasattr(self, 'y_pred_gmm'):

              in1 = self.y_pred_gmm.copy()
              #in1[self.mask] = np.nan

              plot_confmatGMM(in1, self.Lc.copy(), self.bed, self.prefix.get())

              self.plot7_btn.configure(fg='#d64161', background="white")

              del in1
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Error", "Run GMM model first!") 

	#=======================
	def _plot_cm_crf(self):
           """
           this function ...
           """
           if hasattr(self, 'y_pred_crf'):

              in1 = self.y_pred_crf.copy()
              #in1[self.mask] = np.nan

              plot_confmatCRF(in1, self.Lc.copy(), self.bed, self.prefix.get())

              self.plot8_btn.configure(fg='#d64161', background="white")

              del in1
              self.update()
              tkMessageBox.showinfo("Done!", "Plot made") 

           else:
              tkMessageBox.showinfo("Error", "Run CRF model first!") 


	#==============================================================
	#========END functions for plot tab

	#==============================================================
	#==============================================================
	#========END plot tab


	#==============================================================
	#==============================================================
	#========START export tab

	# Populate the second pane. Note that the content doesn't really matter
	export_frame = Tkinter.Frame(nb)
	nb.add(export_frame, text='Export')#, state='disabled')

	export_frame.configure(background='#008B8B')

	Read_msg = [
	    "INSTRUCTIONS:\n\n",
	    "1. On previous tab, set file prefix\n\n"
	    "2. Press buttons to export results!\n"
            "   GMM & CRF raster tifs = substrate maps, geotif format\n" 
            "   GMM raster tif = substrate map, geotif format\n" 
            "   CRF raster tif = substrate map, geotif format\n" 
            "   Bed observations = bed observations, csv and shapefile format\n" 
            "   All data = substrate map(s) in geotif format, probability rasters, bed observations\n" 
             ]


	lbl2 = Tkinter.Label(export_frame, wraplength='4i', justify=Tkinter.LEFT, anchor=Tkinter.N,
		        text=''.join(Read_msg))

	lbl2.configure(background='#DC143C', fg="white")
		        
	# position and set resize behavior
	lbl2.grid(row=0, column=0, columnspan=1, sticky='new', pady=5)

	#=======================
	# check button for export 1 
	self.export1_btn = Tkinter.Button(export_frame, text='GMM & CRF raster tifs', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _export1(self))
	self.export1_btn.grid(row=1, column=0, pady=(2,4))
	self.export1_btn.configure(background='#DC143C', fg="white")

	#=======================
	# check button for export 2 
	self.export2_btn = Tkinter.Button(export_frame, text='All data', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _export2(self))
	self.export2_btn.grid(row=1, column=1, pady=(2,4))
	self.export2_btn.configure(background='#DC143C', fg="white")


	#=======================
	# check button for export 3
	self.export3_btn = Tkinter.Button(export_frame, text='GMM raster tif', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _export3(self))
	self.export3_btn.grid(row=2, column=0, pady=(2,4))
	self.export3_btn.configure(background='#DC143C', fg="white")

	#=======================
	# check button for export 4 
	self.export4_btn = Tkinter.Button(export_frame, text='CRF raster tif', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _export4(self))
	self.export4_btn.grid(row=2, column=1, pady=(2,4))
	self.export4_btn.configure(background='#DC143C', fg="white")

	#=======================
	# check button for export 5
	self.export5_btn = Tkinter.Button(export_frame, text='Bed observations', underline=0,
		         command=lambda filt_heading=self.DATfilename.get(): _export5(self))
	self.export5_btn.grid(row=3, column=0, pady=(2,4))
	self.export5_btn.configure(background='#DC143C', fg="white")


	#==============================================================
	#========START functions for export tab

	#=======================
	def _export1(self):


           if hasattr(self, 'y_pred_gmm') and hasattr(self, 'y_pred_crf'):
              in1 = self.y_pred_gmm.copy()
              in2 = self.y_prob_gmm.copy()
		   
              export_gmm_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())
			  
              in1 = self.y_pred_crf.copy()
              in2 = self.y_prob_crf.copy()
			  
              export_crf_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())

              self.export1_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Data exported") 

           else:
              tkMessageBox.showinfo("Error", "Analyze data first!") 

	#=======================
	def _export2(self):

           if hasattr(self, 'y_pred_gmm') and hasattr(self, 'y_pred_crf'):
              in1 = self.y_pred_gmm.copy()
              in2 = self.y_prob_gmm.copy()
		   
              export_gmm_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())
			  
              in1 = self.y_pred_crf.copy()
              in2 = self.y_prob_crf.copy()
			  
              export_crf_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())

              export_bed_data(self.bed, self.prefix.get())

              self.export2_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Data exported") 

           else:
              tkMessageBox.showinfo("Error", "Analyze data first!") 


	#=======================
	def _export3(self):

           if hasattr(self, 'y_pred_gmm'):
              in1 = self.y_pred_gmm.copy()
              in2 = self.y_prob_gmm.copy()
		   
              export_gmm_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())
			  
              self.export3_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Data exported") 

           else:
              tkMessageBox.showinfo("Error", "Analyze data first!") 

	#=======================
	def _export4(self):

 
           if hasattr(self, 'y_pred_crf'):
              in1 = self.y_pred_crf.copy()
              in2 = self.y_prob_crf.copy()
			  
              export_crf_gtiff(self.mask, in1, in2, self.bs, self.prefix.get())
			  
              self.export4_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Data exported") 

           else:
              tkMessageBox.showinfo("Error", "Analyze data first!") 

	#=======================
	def _export5(self):

 
           if hasattr(self, 'bed'):
              export_bed_data(self.bed, self.prefix.get())

              self.export5_btn.configure(fg='#d64161', background="white")
              self.update()
              tkMessageBox.showinfo("Done!", "Data exported") 

           else:
              tkMessageBox.showinfo("Error", "Read in data first!") 


	#==============================================================
	#========END functions for export tab

	#==============================================================
	#==============================================================
	#========END export tab


	# start app
	master.mainloop()

##-------------------------------------------------------------
if __name__ == '__main__':

   print("""
    ____  ____  ___ ____  __  __     
   |  _ \|  _ \|_ _/ ___||  \/  |  _ 
   | |_) | |_) || |\___ \| |\/| | (_)
   |  __/|  _ < | | ___) | |  | |  _ 
   |_|   |_| \_\___|____/|_|  |_| (_)
                                     
   ___                 _      _                  __                   __      
    | _  _ ||_  _ \/ _|__ ._ |_).__ |_  _.|_ o|o(__|_o _  /\  _ _    (__|_o _ 
    |(_)(_)||_)(_)/\  |(_)|  |  |(_)|_)(_||_)|||__)|_|(_ /--\(_(_)|_|__)|_|(_ 
                                                                              
    __                                          
   (_  _  _|o._ _  _ .__|_ |\/| _.._ ._ o._  _  
   __)(/_(_||| | |(/_| ||_ |  |(_||_)|_)|| |(_| 
                                  |  |       _| 

   |b|y| |D|a|n|i|e|l| |B|u|s|c|o|m|b|e|
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |d|a|n|i|e|l|.|b|u|s|c|o|m|b|e|@|n|a|u|.|e|d|u|

   """)

   gui()


