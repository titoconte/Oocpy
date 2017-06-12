#
# author : Tito Conte [tito.conte@tetratech.com]
# Date: 10/06/2017


#_________________________________________________________________

# libraries
# to shape
import geopandas as gpd
# to math operations
import numpy as np
# to plot
import matplotlib.pyplot as plt
# to list files in directory
from glob import glob
from matplotlib.colors import LogNorm
import sys, os
import seaborn as sns
import pandas as pd
from shapely.geometry import Polygon
#________________________________________________________________

# definitions
#seborn definition
sns.set_style("whitegrid", { 
	                         'grid.color'    : ".5",
	                         'axes.edgecolor': "0",
	                         'legend.frameon': True,
							 'axes.linewidth': 1.5,
							 'axes.grid': True,
							 'grid.color': "0",
							 'grid.linestyle': u'--',
							 'axes.facecolor': '#DAE3FE'
	                       }
	         )

def DynStats(refname):
	''' 
		Definition to dialog water columns files in probabilistic results
		The results are worst and mean case for distance and concentration

		refname(string)
		Scenario sufix name to process
	'''
	# get list of files
	fnames = glob(refname+'*.DYN')

	# start max dist equals 0
	DistMax=0
	# loop in files name
	for fname in fnames:
		# read dyn file
		df = pd.read_table(fname,sep='\s+',skiprows=2)
		# Calculates horizontal distance
		df['distance']=(df.CX**2+df.CZ**2)**0.5
		# checks the scenario maximum distance is "the maximum of maximuns"
		if DistMax<df['distance'].max():
			DistMax=df['distance'].max()

	return DistMax

def PlnResultsIntegrates(refname,px,py,epsg):
	'''
	Integrates PLN results in a unique file and exports shapefile

	refname(string)
		Scenario sufix name to process
	'''
	# get list of files
	fnames = glob(refname+'*.PLN*')

	# loop in files name
	for fname in fnames:
		# reads pln file
		# if final gdf exists ignore results
		if 'Fgdf' in locals():
			try:
				# converts file to dataframe
				gdf = ReadPLN(fname,px,py,epsg)
				# concatenates
				Fgdf = gpd.GeoDataFrame(pd.concat([Fgdf,gdf]))
				# gets maximum thickness
				thickness = Fgdf.groupby(['x','y'],as_index=False).max()
				Fgdf = Fgdf.drop_duplicates(['x','y'])
				Fgdf['thickness']=thickness['thickness'].values
			except:
				print('error in scenario {}'.format(fname))
				pass
		else:
			try:
				# creates final dataframe
				Fgdf = ReadPLN(fname,px,py,epsg)

			except:
				print('error in scenario {}'.format(fname))
				pass

	return Fgdf

def ReadPLN(fname,px,py,epsg,esp=1000,tfac=1,cut=0.01):
	# get the gridsize information
	f = open(fname);
	f.readline();
	f.readline();
	line = f.readline();
	line = line.replace('\r\n','').split(' ');
	iy,ix,dfeet,nx,ny = [float(i) for i in line if i!=''];
	
	ix = ix/dfeet
	iy = iy/dfeet
	
	dx=dfeet*0.3048
	dy=dfeet*0.3048
	
	# grid limits
	yend = py+iy*dy;
	yini = py-(ny-ix)*dy;
	xend = px+(nx-iy)*dx;
	xini = px-iy*dx;
	
	# create grid
	# vectors
	x = np.linspace(xini,xend,nx);
	y = np.linspace(yini,yend,ny);
	
	# grids
	gx,gy = np.meshgrid(x,y)
	# calculates distances
	distance = ((gx-px)**2+(gy-py)**2)**0.5/1000.
	
	# output integrate result
	int_pln = gx*0
	
	# gets pln info
	pln = tfac*np.genfromtxt(fname,skip_header=4)*(453.592/float((dfeet*0.092903)))/float(esp)
	
	# grid the pln
	gi_pln = np.reshape(pln,(int(ny),int(nx)),'C')

	# masked data
	g_pln = np.ma.masked_less_equal(gi_pln,cut)

	# prepate values to create geodataframe
	X = gx.flatten()
	Y = gy.flatten()
	pln = g_pln	.flatten()

	X=X[~pln.mask]
	Y=Y[~pln.mask]
	pln=pln[~pln.mask]

	Dx=dx/2.
	Dy=dy/2.
	# creates polygon
	geometry=[Polygon([(x-Dx,y-Dy),(x+Dx,y-Dy),(x+Dx,y+Dy),(x-Dx,y+Dy),(x-Dx,y-Dy)]) for x,y in zip	(X,Y)]
	# creates geodataframe
	gdf = gpd.GeoDataFrame(
		np.vstack((pln,X,Y)).T,
		columns=['thickness','x','y'],
		geometry=geometry,
		crs={'init':'epsg:'+str(epsg)}
		)
	
	g_pln = np.ma.masked_less_equal(g_pln,0.01)
	ax = plt.subplot(111)
	# pcolor, cmap viridis (best brightness)
	plt.contourf(gx,gy,g_pln,cmap = plt.cm.YlOrBr,norm=LogNorm(vmin=0.01, vmax=10000))
	plt.plot(px,py,'s',color='limegreen')
	# colorbar
	cb  = plt.colorbar(ticks=[0.001,0.01,0.1,1,10,100,1000,10000],drawedges=True)	
	#cb.ax.set_yticklabels(['0',r'10$^{-2}$',r'10$^{-1}$',r'10$^{0}$',r'10$^{1}$',r'10$^{2}$',r'10$^{3}$',r'10$^{4}$'])
	# title
	#cb.set_label('Espessura')
	# labels
	#plt.xlabel('X Coordenadas em UTM (Datum - WGS84)')
	#plt.ylabel('Y Coordenadas em UTM (Datum - WGS84)')
	#cb.ax.set_title('mm')
	#plt.title(outputname.replace('.hst',''))
	plt.show()
	return gdf	

