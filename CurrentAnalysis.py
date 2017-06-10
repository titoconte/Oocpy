# -*- coding: iso-8859-15 -*-

# user definitions
# set window in time step numbers

import sys

import warnings
warnings.filterwarnings("ignore")
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import seaborn as sns
import shapefile, sys
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator,DateFormatter,date2num
import datetime
#sys.path.insert(0, '/home/tbctools/MF_analises/')
#from hist_dir import *

sns.set_style('whitegrid')

def CurrentStickPlot(u,v,times,params={},title=False,figname=False,logo=[0.05,0.05],label_scale=None):
	'''
		
		scale       = params['scale']
		label_scale = params['label_scale']
		step        = params['step']
		dayloc      = params['dayloc']
	'''
	sns.set_context("notebook", font_scale=1.3)

	ntimes = pd.date_range(times[0],times[-1],freq='H')
	inew = np.linspace(0,len(ntimes),len(ntimes))
	ii = np.linspace(0,len(ntimes),len(times))
	u = np.interp(inew,ii,u)
	v = np.interp(inew,ii,v)
	vel = (u*u+v*v)**0.5
	#times = df.index.values
	
	scale       = label_scale/100.
	step        = 1
	
	if label_scale==None:
		if np.max(vel)>=0.5:
			velrange=0.1
			rnumber = 10.
		else:
			velrange=0.01
			rnumber = 100.
		
		velhist = np.histogram(vel,bins=np.arange(-velrange,np.max(vel),velrange))
		#label_scale = round(velhist[1][np.argmax(velhist[0])+1]*rnumber)/rnumber

	y = np.zeros_like(u)	
	x=[]
	for t in ntimes: x.append(date2num(t))

	fig,ax = plt.subplots(nrows=1,ncols=1,figsize=(18, 3))
	

	props = {'units'         : "dots",
			 'width'         : 2,
			 'headwidth'     : 0,
			 'headlength'    : 0,
			 'headaxislength': 0,
			 'scale'         : scale,
			 }

	unit_label = "%3g %s"%(label_scale, 'm/s')
	Q = ax.quiver(x[::step], y[::step], u[::step], v[::step],angles='uv', **props)
	kw = {'coordinates':'axes', 'labelpos':'S'}
	ax.quiverkey(Q, X=0.05, Y=0.95, U=label_scale, label=unit_label, coordinates='axes', labelpos='S')
	
	
	yaxis = ax.yaxis
	xaxis = ax.xaxis
	yaxis.set_ticklabels([])

	ax.grid(True)

	plt.axis("tight")

	ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
	#ax.xaxis.set_major_locator(DayLocator(5))
	#plt.gca().xaxis_date()
	plt.gca().get_autoscalex_on

	ax.axes.get_yaxis().set_visible(False)

	utils.insertlogo(ax,logo[0],logo[1])

	plt.title('Stickplot',fontsize=14)

	plt.savefig(figname+'.png',dpi=300,bb_box='tight')

	plt.close()

def WriteHST(P,D,prof,fname):
	
	ntime,nprofs = P.shape

	with open(fname,'w') as f:
		for i in range(ntime):
			f.write('-{}\r\n'.format(nprofs))
			for p,j,d in zip(prof,np.squeeze(P[i,:]),np.squeeze(D[i,:])):
				f.write('   {:10.2f}     {:10.6f}     {:10.6f}\r\n'.format(p,j,d))

def GetsData(fname,xflag='lon',yflag='lat',zflag='depth',tflag='time',uflag='u',vflag='v',lat=None,lon=None):
	
	# open dataset
	ds = xr.open_dataset(fname)
	
	# rename varibles dataset
	flags={uflag:'u',vflag:'v',zflag:'depth',tflag:'time',xflag:'lon',yflag:'lat'}
	
	ds.rename(flags,inplace=True)
	
	# if necessary get point
	if (lon!=None) & (lat!=None):
		ds = ds.sel(lon=lon,lat=lat,method='nearest')
	# converts to dataframe
	df = ds[['u','v']].squeeze().to_dataframe().dropna().drop(['lon','lat'],axis=1)

	# order multindex
	df = df.swaplevel('time','depth')
		
	return df
	
def InterpTimeDataFrame(df,InterpFreq='H',InterpCalc='linear',**kwargs):
	
	time = df.index.get_level_values('time')
	newtime = pd.date_range(time.min(),time.max(), freq=InterpFreq)
	
	newindex=pd.MultiIndex.from_product(
			iterables=[
				newtime,
				df.index.get_level_values('depth').unique()
			],
			names=['time','depth']
		)
	
	df = df.reindex(newindex)
	
	df = df.interpolate(InterpCalc,**kwargs)
	
	return df

def ThetaCalcuation(D,bins=72):

	v,b = np.histogram(D,bins)
	b=np.round(b)
	nmax = np.argmax(v)
	theta=(b[nmax]+b[nmax+1])/2.

	if nmax>0:
		if 0.85*v.max()<=v[nmax-1]:
			theta=bins[nmax]

	if 0.85*v.max()<=v[nmax+1]:
			theta=bins[nmax+1]	

	return np.radians(theta)

def RotationVectors(u,v,theta):
	
	ut=u*np.cos(theta)-v*np.sin(theta)
	vt=u*np.sin(theta)+v*np.cos(theta)

	return ut,vt

if __name__=='__main__':
	
	
	windowstep = 24*30
	uflag = 'U'
	vflag = 'V'
	zflag = 'DEPTH1_17'
	tflag = 'time'
	xflag = 'X3144_3144'
	yflag = 'Y1403_1403'
	MyProfs=[0,50,150,250,500,700]
	#DataPath='../../D_Dados/corrente/'
	DataPath=''
	fname = glob('../*.nc')[0]
	
	# Gets data
	df = GetsData(fname,xflag,yflag,zflag,tflag,uflag,vflag)
	# interpolates results
	df = InterpTimeDataFrame(df)
	
	# calculates velocity and direction
	df['velocity']=df.u**2+df.v**2
	df['direction'] = np.degrees(np.arctan2(df.u,df.v))
	df.loc[df['direction']<0,'direction']+=360
	
	# find turn points
	theta=ThetaCalcuation(df['direction'].values)


	thickness = np.diff(np.asarray(MyProfs))
	thickness.loc[0]=10

