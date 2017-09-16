
import numpy as np
import geopandas as gpd
import pandas as pd 
import xarray as xr
from shapely.geometry import Point


class OocInputs:
	'''
		discharges dictionary with :
			rate (lb/gl)
			ratio meters??
			depth (meters)
			angle (degrees)
			azimuth (degrees)
			x (grid value)
			y (grid value)
			time(hours)
	'''
	def __init__(self,x,y,Depth=1000,StudyName=None,epsg='4326'):
		self.StudyName=StudyName
		self._gdf=gpd.GeoDataFrame([Depth],geometry=[Point([x,y])],columns=['depth'],crs={'init':'epsg:{}'.format(epsg)})
		self._gdf = self._gdf.to_crs({'init':'epsg:4326'})
		# grid definition
		self.nx=110
		self.ny=110
		self.nt=75
		# OOC flags
		self.NOSQUEEZE=True
		self.FULL=True
		self.PVALL=True
		self.REVPLAN=True
		self.SAVEDYN=True
		# cell size
		self.CellSize=40.
		# sea state to OOC
		self.SeaState1=0.
		self.SeaState2=8.
		self.SimulationTime=1000000
		self.TimeStepSeconds=3600
		self.comments=['MUD']
		self._breaklines=''.join(np.repeat('1234567890',1))
		self.discharge={
			'rate':39.76,
			'ratio':0.35,
			'depth':3279.20,
			'angle':-45,
			'azimuth':0,
			'x':2200,
			'y':2200,
			'time':270000,
			'bulk':9.97,
			'composition':{}
		}
		self.lon, self.lat =self._gdf.geometry.bounds.iloc[:,2:].values[0]
		self.CurrFileName=None
		self.MyProfs=[0,50,150,250,500,700]
		self.density={}		
		self.CurrProfile=[]
		self.CurrLayers=6

	def GetCurrent(self):
		#try:
		f = open(self.CurrFileName,'r')
		self.CurrProfile = f.readlines()
		f.close()
		#except:
			#print('Define CurrFileName')
			#pass

		return self
	
	def WriteIni(self,filename):
	
		with open(filename,'w') as f:
			f.write(self.comments[0])
			
			f.write('\n'+self._breaklines)
			if self.NOSQUEEZE:
				f.write('\nNOSQUEEZE\n')
			if self.FULL:
				f.write('\nFULL\n')
			if self.PVALL:
				f.write('\nPVALL\n')
			if self.REVPLAN:
				f.write('\nREVPLAN\n')
			if self.SAVEDYN:
				f.write('\n\nSAVEDYN\n')
			f.write('\n\nGRID\n')
			f.write('{} {}\n'.format(self.nx,self.ny))
			f.write('{0:.1f}\n'.format(self.CellSize))
			f.write('CONSTANT\n{0:.2f}\n'.format(self._gdf.depth.values[0]*3.28084))
			f.write('\nDISCHARGE\n')
			f.write('{rate:.2f}, {ratio:.2f}, {depth:.2f}, {angle:.1f}, {azimuth:.1f}\n'.format(**self.discharge))
			f.write('{x:.2f} {y:.2f}\n'.format(**self.discharge))
			f.write('{time:.1f}\n'.format(**self.discharge))
			f.write('{bulk:.2f}\n'.format(**self.discharge))
			for key,val in sorted(self.discharge['composition'].items()):
				f.write('"{}" {:.1f} {:.5f} {:.5f}\n'.format(key,*val))
			
			f.write('\nAMBIENT\n')
			f.write('3 {} {}\n'.format(self.nt,self.TimeStepSeconds))
			f.write(''.join(self.CurrProfile))
			f.write('1 {}\n'.format(len(self.density)))
			for key,val in sorted(self.density.items()):
				f.write('{} {} \n'.format(key,val))
			f.write('{}\n'.format(1))
			f.write('{0:.2f} {1:.2f}\n'.format(float(self.SeaState1),float(self.SeaState2)))
			f.write('\nOUTPUT\n')
			f.write('0 0 1 1 10\n')
			f.write('5\n')
			f.write('0\n')
			f.write('0\n')
			f.write('0 0 0\n')
			f.write('0\n')
			f.write('-{}\n'.format(len(self.density)))
			f.write(' '.join(sorted(list(self.density.keys()))))
			f.write('\nALLSOLIDS\n')
			f.write('BO\n')
			f.write('3 {0:.1f} -1\n'.format(self.SimulationTime))
			f.write('\nTIMESTEP\n')
			f.write('{}\n'.format(self.TimeStepSeconds))
			
			f.write('\nEND\n')
	
	def ProbGeneration(self,fname,step=1,windows=False):
		
		self = self.GetCurrent()
		N=len(self.CurrProfile)
		Nlayers=self.CurrLayers+1
		Nlim=N-(self.nt)*Nlayers
		i=0
		k=0
		if windows:
			ftype='bat'
			oocfname='oc120299'
			copycommand='copy'
		else:
			ftype='sh'
			oocfname='wine oc120299.exe'
			copycommand='cp'

		f = open(fname+'_run.'+ftype,'w')

		while i < Nlim:
			self = self.GetCurrent()
			self.CurrProfile=self.CurrProfile[i:(self.nt*Nlayers+i)]
			self.WriteIni('{}_{:04d}.in'.format(fname,k))
			
			f.write('{} {}_{:04d}.in {:04d}.out >> {:04d}.txt\n'.format(oocfname,fname.split('/')[-1],k,k,k))
			f.write(copycommand+' DYNPLUME {}_{:04d}.DYN\n'.format(fname.split('/')[-1],k))
			f.write(copycommand+' PLANVW {}_{:04d}.PLN\n'.format(fname.split('/')[-1],k))
			
			k+=1
			i+=Nlayers*step
		f.close()



def GetDensityFromWOA13(depth,lon,lat,self,periods={'intense':1.5,'weak':4.5}):

		density={}
		
		OPENDAPprefix='https://data.nodc.noaa.gov/thredds/dodsC/woa/WOA13/DATAv2/temperature/netcdf/decav/0.25/woa13_decav_'
		
		OPENDAPsufix='_04v2.nc'
		
		# gets files opendap access
		FullURLtemp = lambda x:OPENDAPprefix+'t{:02d}'.format(x)+OPENDAPsufix 
		
		FullURLsal = lambda x:OPENDAPprefix+'s{:02d}'.format(x)+OPENDAPsufix 
		
		# gets files opendap access
				
		if depth.values[0]>1500:
			print('WOA13 profile will generate with climatology data')
			DataRange=list(range(13,17))
		else:
			print('WOA13 profile will generate with monthly data')
			DataRange=list(range(1,13))
		
		# creates a dataset list
		ListWOA13Data = list(map(FullURLtemp,DataRange))+list(map(FullURLsal,DataRange))
		print(ListWOA13Data)
		# Converts to dataset
		ds = xr.open_mfdataset(ListWOA13Data,decode_times=False)
		
		# Gets closer point and converts to DataFrame and remove invalid data
		df = ds[['s_an','t_an']].sel(lon=lon,lat=lat,method='nearest').to_dataframe().dropna()
		
		ds.close()
	
		# calculates pressure
		df['pressure'] = gsw.p_from_z(df.index.get_level_values('depth'),ds['lat'].values)
		# calculates absolut salinity
		df['AbsSal']=gsw.deltaSA_from_SP(df['s_an'].values,df['pressure'],df['lon'].values,df['lat'].values)
		# calculates density
		df['density'] = gsw.rho_t_exact(df['AbsSal'].values,df['t_an'].values,df['pressure'].values)

		# export denity profiles
		for key,val in periods.iteritems():
			# exports data
			df.xs(val,level='time',axis=0,drop_level=False)['density'].to_csv('DensityProfiles_{}.csv'.format(key),sep=';')
			
			density[key]=df.xs(val,level='time',axis=0,drop_level=False)['density']
	
		return density



if __name__=='__main__':
	
	x=338427
	y=9097511
	epsg=32725
	Depth=700

	i=0
	forte=OocInputs(x,y,Depth,StudyName='17028',epsg=epsg)

	forte.CurrFileName='../hycom_fraco.hst'
	forte.discharge['depth']=2288.39
	forte.discharge['rate']=80.50
	forte.discharge['time']=85788.
	forte.discharge['x']=2200
	forte.discharge['y']=3300
	forte.nt=35
	forte.SimulationTime=126000.
	forte.discharge['composition']={
		"sol1":[2.6, 0.83166, 0.83166 ],
		"sol2":[2.6, 0.00009, 0.43726],
		"sol3":[2.6, 0.00217, 0.43251],
		"sol4":[2.6, 0.00232, 0.31312],
		"sol5":[2.6, 0.00261, 0.12744],
		"sol6":[2.6, 0.00051, 0.12521],
		"sol7":[2.6, 0.00029, 0.04567]
	}

	
	forte.density={
		'0':1.0236,
		'0328.08':1.0256,
		'1640.42':1.0294,
		'2296.59':1.0308
	}
	
	fname='../OOC/pepb_PI_fraco'
	forte.ProbGeneration(fname)



	#a.GetDensityFromWOA13()