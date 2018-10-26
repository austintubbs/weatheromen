from buoy import buoy
import numpy as np
import datetime
# import urllib
import time
from netCDF4 import Dataset
from urllib.request import urlopen
from buoyUtils import getHumanTimestamp

class CDIPbuoy(buoy):
       # Represents a CDIP wave buoy
    def __init__(self,name,number,localTimeOffset):  #Name, Station Number, and Local Time Offset in Hours
        """Initializes the data."""
        self.name = name
        self.number = str(number)
        self.localTimeOffset = localTimeOffset*3600
        super().__init__(name,number,localTimeOffset) # not sure what this does but it was recommended
    
    def loadNetCDF(self,daysToLoad):
        t0 = time.time() # time data started loading
        
        # Load wave data time series from netcdf
        urlarc = 'http://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/' + self.number + 'p1_rt.nc'
        nc = Dataset(urlarc)
        self.timeUnix = nc.variables['waveTime'][0:2] # Get first two times
        self.dt = self.timeUnix[1]-self.timeUnix[0] # Calculate the difference between times
        tStart = -int((daysToLoad*86400*1.2)/(self.dt)) # Find desired start time
        self.timeUnix = nc.variables['waveTime'][tStart:-1] # Load time vector
        self.nt = len(self.timeUnix)
        # Create datetime lists for UTC and local times
        self.dateTimeUTC = []
        self.dateTimeLocal = []
        for i in range(0,self.nt):
            self.dateTimeUTC.append(datetime.datetime.utcfromtimestamp(self.timeUnix[i]))
            self.dateTimeLocal.append(datetime.datetime.utcfromtimestamp(self.timeUnix[i]+self.localTimeOffset))
        # Load wave data
        self.waveBandwidth = nc.variables['waveBandwidth'][:]
        self.waveFrequency = nc.variables['waveFrequency'][:]
        self.wavePeriod = 1/self.waveFrequency
        self.waveEnergyDensityGrid = nc.variables['waveEnergyDensity'][tStart:-1,:]
        self.waveMeanDirectionGrid = nc.variables['waveMeanDirection'][tStart:-1,:]
        self.waveHs = nc.variables['waveHs'][tStart:-1]
        self.DPD = nc.variables['waveTp'][tStart:-1]
        self.waveTa = nc.variables['waveTa'][tStart:-1]
        self.MWD = nc.variables['waveDp'][tStart:-1]
        # Create frequency and direction bin coordinates for colormap plots
        self.frequencyBins = np.append(self.waveFrequency - (self.waveBandwidth/2), self.waveFrequency[-1] + (self.waveBandwidth[-1]/2))
        self.directionBins = np.asarray(np.arange(2.5,367.5,5)) #range(0,360,10)
        
        # Load historical 2D wave energy direction spectrum from CDIP website
        self.waveEnergyDensityDirectionGrid = np.zeros((self.nt+1,64,72))
        self.url = []
        for i in range(self.nt+1):
            if i == self.nt:
                self.url.append('http://cdip.ucsd.edu/data_access/MEM_2dspectra.cdip?' + self.number)
            else:
                humanDate = getHumanTimestamp(self.timeUnix[i], '%Y%m%d%H%M') # Convert unix timestamp to string format to attach to URL
                # save urls for debugging purposes
                self.url.append('http://cdip.ucsd.edu/data_access/MEM_2dspectra.cdip?sp' + self.number + '01' + humanDate)
            data = urlopen(self.url[i])
            readdata = data.read().decode("utf-8") # Read text file of recent data
            datas = readdata.split("\n") # Split text file into individual rows
            datas2 = []
            for item in datas:
                 line = item.strip().split()
                 datas2.append(line) 
            datas2[0].remove('<pre>')
            datas2[64].remove('</pre>')
            datas2.pop()
            Edarray = np.asarray(datas2, dtype=object)
            self.waveEnergyDensityDirectionGrid[i] = np.double(Edarray)
        #  Load recent 2D wave energy direction spectrum from CDIP website
        
        self.waveDirection  = np.arange(5,365,5)
        
        t1 = time.time()
        total = t1-t0
        print(self.name,"data loaded in %.1f seconds"%total)