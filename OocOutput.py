#
# author : Tito Conte [tito.conte@tetratech.com]
# Date: 10/06/2017


#_________________________________________________________________

# libraries
# to shape
from geopandas import GeoDataFrame
# to math operations
import numpy as np
# to plot
import matplotlib.pyplot as plt
# to list files in directory
from glob import glob
from matplotlib.colors import LogNorm
import seaborn as sns
import pandas as pd
from shapely.geometry import Polygon,Point
from shutil import copyfile
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
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

def DynStats(refname,moveMain=None):
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
		df = df.loc[df.TSSC>5,:]
		# Calculates horizontal distance
		df['distance']=((df.CX*0.3048)**2+(df.CZ*0.3048)**2)**0.5
		# checks the scenario maximum distance is "the maximum of maximuns"
		if DistMax<df['distance'].max():
			DistMax=df['distance'].max()
			ffname=fname
	print(ffname)
	print(DistMax)
	if moveMain!=None:
		copyfile(ffname,moveMain+ffname.split('\\')[-1])
	return [DistMax,df.TSSC.max()]

def PlnResultsIntegrates(refname,px,py,epsg,wannaview=False,tfac=1):
	'''
	Integrates PLN results in a unique file and exports shapefile

	refname(string)
		Scenario sufix name to process
	'''
	# get list of files
	fnames = glob(refname+'*.PLN*')
	N=100/float(len(fnames))

	# loop in files name
	for fname in fnames:
		# reads pln file
		# if final gdf exists ignore results
		if 'Fgdf' in locals():
			try:
				# converts file to dataframe
				gdf = ReadPLN(fname,px,py,epsg,tfac=tfac)
				gdf['prob001']=(gdf['thickness'].values>0.01)*1
				gdf['prob01']=(gdf['thickness'].values>0.1)*1
				gdf['prob1']=(gdf['thickness'].values>1)*1
				gdf['prob10']=(gdf['thickness'].values>10)*1
				# concatenates
				Fgdf = GeoDataFrame(pd.concat([Fgdf,gdf]))
				# gets cocorrence
				prob = Fgdf.groupby(['x','y'],as_index=False).sum()
				prob = prob.sort_values(['x','y'])
				# gets maximum thickness
				thickness = Fgdf.groupby(['x','y'],as_index=False).max()
				thickness=thickness.sort_values(['x','y'])
				Fgdf = Fgdf.drop_duplicates(['x','y'])
				Fgdf = Fgdf.sort_values(['x','y'])
				Fgdf['thickness']=thickness['thickness'].values
				Fgdf['prob001'] = prob['prob001'].values
				Fgdf['prob01']  = prob['prob01'].values
				Fgdf['prob1']   = prob['prob1'].values
				Fgdf['prob10']  = prob['prob10'].values
			except:
				print('error in scenario {}'.format(fname))
				pass
		else:
			try:
				# creates final dataframe
				Fgdf = ReadPLN(fname,px,py,epsg,wannaview=wannaview)
				Fgdf['prob001'] =(Fgdf['thickness'].values>0.01)*1
				Fgdf['prob01']  =(Fgdf['thickness'].values>0.1)*1
				Fgdf['prob1']   =(Fgdf['thickness'].values>1)*1
				Fgdf['prob10']  =(Fgdf['thickness'].values>10)*1

			except:
				print('error in scenario {}'.format(fname))
				pass;
	Fgdf['prob001']=Fgdf['prob001'].values*N
	Fgdf['prob01']=Fgdf['prob01'].values*N
	Fgdf['prob1']=Fgdf['prob1'].values*N
	Fgdf['prob10']=Fgdf['prob10'].values*N
	return Fgdf

def ReadPLN(fname,px=338427,py=9097511,epsg=32725,esp=2700,
			tfac=1,cut=0.01,wannaview=False,english=False,
			figformat=None,extent=None,xlocator=None,ylocator=None):
	# get the gridsize information
	if isinstance(fname,str):
		f = open(fname);
	elif isinstance(fname,list):
		f = open(fname[0]);
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
	yini = py-(ny-iy)*dy;
	xend = px+(nx-ix)*dx;
	xini = px-ix*dx;

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
	if isinstance(fname,str):
		# check the dfeet
		pln = tfac*np.genfromtxt(fname,skip_header=4)*(453.592/float((dfeet*dfeet*0.092903)))/float(esp)
	elif isinstance(fname,list):
		for f in fname:
			if 'pln' in locals():
				pln+= tfac*np.genfromtxt(f,skip_header=4)*(453.592/float((dfeet*0.092903)))/float(esp)
			else:
				pln = tfac*np.genfromtxt(f,skip_header=4)*(453.592/float((dfeet*0.092903)))/float(esp)
	# grid the pln
	gi_pln = np.reshape(pln,(int(ny),int(nx)),'C')

	# masked data
	g_pln = np.ma.masked_less_equal(gi_pln,cut)

	# prepate values to create geodataframe
	X = gx.flatten()
	Y = gy.flatten()
	pln = g_pln.flatten()

	X=X[~pln.mask]
	Y=Y[~pln.mask]
	Xf=X+dx
	Yf=Y+dy
	pln=pln[~pln.mask]
	maxpln = dx*0.6*1000
	if pln.max()>maxpln:
		print('o cenario {} apresenta espesuras acima de {} e portanto foi balizado'.format(fname,maxpln))
		pln[pln>maxpln]=maxpln

	# creates polygon
	geometry=[Polygon([(xi,yi),(xf,yi),(xf,yf),(xi,yf),(xi,yi)]) for xi,yi,xf,yf in zip(X,Y,Xf,Yf)]
	# creates geodataframe
	gdf = GeoDataFrame(
		np.vstack((pln,X,Y)).T,
		columns=['thickness','x','y'],
		geometry=geometry,
		crs={'init':'epsg:'+str(epsg)}
		)

	if figformat is not None:

		pt = GeoDataFrame(['pt'],geometry=[Point(px,py)],crs={'init':'epsg:'+str(epsg)})
		pt = pt.to_crs({'init':'epsg:4326'})

		geometry=[Point(max(x),max(y)),Point(min(x),min(y))]
		bnds = GeoDataFrame(['pt','pt2'],geometry=geometry,crs={'init':'epsg:'+str(epsg)},columns=['Name'])

		bnds = bnds.to_crs({'init':'epsg:4326'}).geometry.bounds
		maxx,maxy = bnds[['maxx','maxy']].max()
		minx,miny = bnds[['minx','miny']].min()

		ax = plt.subplot(111)
		# pcolor, cmap viridis (best brightness)
		plt.contourf(gx,gy,g_pln,cmap = plt.cm.YlOrBr,norm=LogNorm(vmin=0.01, vmax=10000))
		plt.plot(px,py,'x',color='black',zorder=10,mew=1.3, ms=5)
		plt.plot(px,py,'o',color='white',zorder=9)
		# colorbar
		cb  = plt.colorbar(ticks=[0.001,0.01,0.1,1,10,100,1000,10000],drawedges=True,pad = 0.25)
		cb.ax.set_yticklabels(['0',r'10$^{-2}$',r'10$^{-1}$',r'10$^{0}$',r'10$^{1}$',r'10$^{2}$',r'10$^{3}$',r'10$^{4}$'])
		if english:
			# title
			cb.set_label('Thickness')
			# labels
			plt.xlabel('X Coordinates UTM (Datum - WGS84)')
			plt.ylabel('Y Coordinates UTM (Datum - WGS84)')
		else:
			# title
			cb.set_label('Espessura')
			# labels
			plt.xlabel('X Coordenadas em UTM (Datum - WGS84)')
			plt.ylabel('Y Coordenadas em UTM (Datum - WGS84)')
		cb.ax.set_title(ur'mm')
		ax.set_aspect('equal')

		if extent is not None:
			ax1 = plt.axes([.4, .6, .4, .34],projection=ccrs.PlateCarree())
			pt.plot(ax=ax1,marker='o', color='red', markersize=5)
			gl = ax1.gridlines(draw_labels=True)
			if xlocator is not None:
				gl.xlocator = mticker.FixedLocator(xlocator)
			if ylocator is not None:
				gl.ylocator = mticker.FixedLocator(ylocator)
			gl.xlabels_top = gl.ylabels_left = False
			gl.ylabels_right = True
			gl.xformatter = LONGITUDE_FORMATTER
			gl.yformatter = LATITUDE_FORMATTER
			gl.xlabel_style = {'size': 10}
			gl.ylabel_style = {'size': 10}
			ax1.set_extent(extent)
			shp = shapereader.Reader('U:/Basemap')
			for record, geometry in zip(shp.records(), shp.geometries()):
				ax1.add_geometries([geometry], ccrs.PlateCarree(),facecolor='lightgray',edgecolor='black')

		# Utils.insertlogo(ax,0.01,0.01,loc=None)
		if isinstance(fname,str):
			plt.savefig(fname.replace('PLN',figformat),dpi=300,bbox_inches='tight',format=figformat)
		elif isinstance(fname,list):
			s1=fname[0].replace('.PLN','')
			for s2 in fname[1:]:
				PluChar=[a2 for a1,a2  in zip(s1,s2) if a1!=a2]
				s1+='_'+''.join(PluChar)
			plt.savefig(s1+'.'+figformat,dpi=300,bbox_inches='tight',format=figformat)
		if wannaview:
			plt.show()

		plt.close()

	return gdf
