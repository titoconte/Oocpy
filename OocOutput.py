#
# author : Tito Conte [tito.conte@tetratech.com]
# Date: 04/02/2016

# How to use?
# put all the scenerio (pln files) wich you want integrate in the same directory
# run the script, if you which, it plots all scenarios
# and integrate this scenarios in one shape
 
#_________________________________________________________________

# libraries
# to shape
import shapefile
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

class OocOutputProcess:

	def __init__(self,path,x,y):
		'''
		path = string
		path where the PLN files are
		
		x;y = float
		Coordinate UTM points
		
		fnames =  list opitional
		sorted PLN file names
		
		Cut = float (optional)
		Thicheness cut default is 0.01
		
		UTMZone = string (optional)
		The UTMZONE number plus S or N hemisphere dependece, default is '24N'
		
		ClassIntervals = list/numpy.array
		Sorted list with thickness classes
		
		PointNames = string
		Point Name default is 'pointname'. 
		It's necessary to use sum definitions (the point name is removed in groupby dataframe process)
		
		ScenarioProperty = dict
		Dictionary where keys are scenario label (likes fase1) with float values for discharged grain size
				
		'''
		self.path=path
		self.fnames=np.sort(glob(self.path+'/*.PLN')
		self.Cut=0.01
		self._TimeFactor=1
		self.UTMZone='24S'
		self._CentralMeridian = -39
		self.ClassIntervals=[0.01,0.1,1,10]
		self.x = 208393.71
		self.y = 1417779.09
		self.PointName='pointname'
		self.ScenarioProperty=dict([])
	
	def ProjectionInfoUTM(self):
		'''
		Calculates central meridian for utmzone
		Used after changes the UTMZone value
		'''
		self.UTMZone=UTMZone
		CentralMeridian = np.arange(-87,-26,6)
		self.CentralMeridian=CentralMeridian[int(UTMZone[:2])-16]
		return self
	
	@staticmethod
	def ReadPLN(fname,px,py,esp=1000,tfac=1,cut=0.01)
		# get the gridsize information
		f = open(fname);
		f.readline();
		f.readline();
		line = f.readline();
		line = line.replace('\r\n','').split(' ');
		ix,iy,dfeet,nx,ny = [float(i) for i in line if i!=''];
		
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
		distance = ((gx-px)**2+(gy-py)**2)**0.5/1000.
		
		# output integrate result
		int_pln = gx*0
		
		# gets pln info
		pln = tfac*np.genfromtxt(fname,skip_header=4)*(453.592/float((dfeet*0.092903)))/float(esp)
		
		# grid the pln
		gi_pln = np.reshape(pln,(nx,ny),'C')
		
		g_pln = np.ma.masked_less_equal(gi_pln,cut)
		
		
		


# to write the outputfile in shape format
def createshape(gx,gy,int_pln,outputname,dx,dy,corte=0.01):
	
	# stack all inputs and remove invalid values (zeros)
	pln = np.hstack(int_pln)
	X = np.hstack(gx)[pln>corte]
	Y = np.hstack(gy)[pln>corte]
	pln = pln[pln>corte]
	
	# write the shapefile
	w = shapefile.Writer(shapefile.POLYGON)
	
	# write fields
	w.field('Espessura','N',20,3)
	
	# loop to all valid values
	for x,y,z in zip(X,Y,pln):
		 
		 # write closed polygon
		 w.poly(parts=[[[x-dx/2.,y-dy/2.],[x+dx/2.,y-dy/2.],[x+dx/2.,y+dy/2.],[x-dx/2.,y+dy/2.],[x-dx/2.,y-dy/2.]]])
		 # write the record correspondent to the polygon above
		 w.record(np.round(z,3))
		
	w.saveShp(outputname)
	w.saveShx(outputname)
	w.saveDbf(outputname)
	with open(outputname+'.prj','w') as f:
		f.write(
		#u'PROJCS["SIRGAS 2000 / UTM zone {}",GEOGCS["SIRGAS 2000",DATUM["D_SIRGAS_2000",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",{}],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",10000000],UNIT["Meter",1]]'.format(utmzone,central_meridian))
		'PROJCS["WGS_1984_UTM_Zone_19N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-69],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')


# to make a fast plot
def fastplot(gx,gy,g_pln,outputname,px,py,wanna_show):
	# mask the pln plot
	g_pln = np.ma.masked_less_equal(g_pln,0.01)
	ax = plt.subplot(111)
	# pcolor, cmap viridis (best brightness)
	plt.contourf(gx,gy,g_pln,cmap = plt.cm.YlOrBr,norm=LogNorm(vmin=0.01, vmax=10000))
	plt.plot(px,py,'s',color='limegreen')
	# colorbar
	cb  = plt.colorbar(ticks=[0.001,0.01,0.1,1,10,100,1000,10000],drawedges=True)	
	cb.ax.set_yticklabels(['0',r'10$^{-2}$',r'10$^{-1}$',r'10$^{0}$',r'10$^{1}$',r'10$^{2}$',r'10$^{3}$',r'10$^{4}$'])
	# title
	cb.set_label('Espessura')
	# labels
	plt.xlabel('X Coordenadas em UTM (Datum - WGS84)')
	plt.ylabel('Y Coordenadas em UTM (Datum - WGS84)')
	cb.ax.set_title(ur'mm')
	plt.title(outputname.replace('.hst',''))
	# Utils.insertlogo(ax,0.01,0.01,loc=None)
	plt.savefig(outputname,bbox_inches='tight',dpi=300)
	# show!
	if wanna_show:
		plt.show()
	plt.close()
	
#_______________________________________________________________		
# main code
if __name__=='__main__':
	
	#iterables = [pname,kind,['max_dist_0.01','max_dist_0.1','max_dist_1','max_dist_10','max_thicks']]
	iterables = [pname,['max_dist_0.01','max_dist_0.1','max_dist_1','max_dist_65','max_thicks']]
	index= pd.MultiIndex.from_product(iterables)
	#index= ['max_dist_0.01','max_dist_0.1','max_dist_1','max_dist_10','max_thicks']
	#itercols = [fases,direction]
	cols=fases
	#cols= pd.MultiIndex.from_product(itercols)
	df = pd.DataFrame(index=index,columns=cols)
	df = df.sortlevel(0)
	path = '.'
	parts = ['']
	for part in parts:

			fnames =  glob(path+'/*.PLN')
			
			
			
			# loop in all outputfiles
			for fname in fnames:
				
				# output name
				outputname = fname.replace('.PLN','')
				
				# load file
				# densidade cascalho
				if ('fase1' in fname):
					tfac=1
					esp = 1084
				elif ('fase2' in fname):
					tfac=1
					esp = 1103
				elif ('fase3' in fname):
					tfac=0.5#1.19
					esp = 2629
				elif('fase4' in fname):
					tfac=1#1.51
					esp = 2624				
				elif('fase5' in fname):
					tfac=1#2.33
					esp = 2618
					
				pln = tfac*np.genfromtxt(fname,skip_header=4)*(453.592/float((dfeet*0.092903)))/float(esp)
				

				
				
				# plot
				if wanna_plot:
					fastplot(gx,gy,g_pln,outputname+'.png',px,py,wanna_show)
				if wanna_shape:
					createshape(gx,gy,g_pln,outputname,dx,dy)
				
				col1 = [fase for fase in fases if fase in outputname]
				#col2 = [dd for dd in direction if dd in outputname]
				row1 = [pp for pp in pname if pp in outputname]
				#row2 = [k for k in kind if k in outputname]
				print('\n'+fname)

				df.loc[(row1,'max_thicks'),(col1)] = np.round(np.max(g_pln))
				
				xx,yy = np.gradient(g_pln)
				angle = np.arctan2(xx,yy)
				D = ((np.sin(angle)*dx)**2+(np.cos(angle)*dy)**2)**0.5
				
				df.loc[(row1,'max_dist_0.01'),(col1)] = np.round(np.max(np.ma.masked_where(g_pln<0.01,distance)),3)
				df.loc[(row1,'max_dist_0.1'),(col1)] = np.round(np.max(np.ma.masked_where(g_pln<0.1,distance)),3)
				df.loc[(row1,'max_dist_1'),(col1)] = np.round(np.max(np.ma.masked_where(g_pln<1,distance)),3)
				df.loc[(row1,'max_dist_65'),(col1)] = np.round(np.max(np.ma.masked_where(g_pln<6.5,distance)),3)

				# sum the results
				int_pln+=gi_pln
				
			int_pln = np.ma.masked_less_equal(int_pln,corte)
			# sum
			if wanna_sum:
				if wanna_plot:
					fastplot(gx,gy,int_pln,outputname+'_soma.png',px,py,wanna_show)
				
				# create shape and integrate
				if wanna_shape:
					createshape(gx,gy,int_pln,outputname+'_soma',dx,dy)
			
				col1 = 'soma'
				#col2 = [dd for dd in direction if dd in outputname]
				row1 = [pp for pp in pname if pp in outputname]
				#row2 = [k for k in kind if k in outputname]
				df.loc[(row1,'max_thicks'),(col1)] = np.round(np.max(int_pln))
				xx,yy = np.gradient(int_pln)
				angle = np.arctan2(xx,yy)
				D = ((np.sin(angle)*dx)**2+(np.cos(angle)*dy)**2)**0.5

				df.loc[(row1,'max_dist_0.01'),(col1)] = np.round(np.max(np.ma.masked_where(int_pln<0.01,distance)),3)
				df.loc[(row1,'max_dist_0.1'),(col1)] = np.round(np.max(np.ma.masked_where(int_pln<0.1,distance)),3)
				df.loc[(row1,'max_dist_1'),(col1)] = np.round(np.max(np.ma.masked_where(int_pln<1,distance)),3)
				df.loc[(row1,'max_dist_65'),(col1)] = np.round(np.max(np.ma.masked_where(int_pln<6.5,distance)),3)
				print('\nSOMA')
	df.to_csv('tabela_diag.csv',sep=';')
	print('\n\n')
	print(df)
	print('\n\n')
	os.system('pause') 

			
	

# plot? (True/False)
wanna_plot = True
wanna_show = False
wanna_sum  = True
wanna_shape = True

fases = ['fase1','fase2','fase3','fase4','fase5','soma']
pname = ['siluro']
