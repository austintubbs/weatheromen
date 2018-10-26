from buoy import buoy
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar
import requests
import time

# Buoy 1 is 273.2 nm from Waimea buoy at 308 deg true
class NOAAbuoy(buoy):
    # Represents a CDIP wave buoy
    def __init__(self, name, stn, localTimeOffset):  # Name, Station Number, and Local Time Offset in Hours
        """Initializes the data."""
        self.name = name
        self.stn = str(stn)
        self.localTimeOffset = localTimeOffset * 3600
        super().__init__(name, stn, localTimeOffset)  # not sure what this does but it was recommended

    def loadData(self, daysToLoad):
        t0 = time.time() # time data started loading
        
        # Pull down the swell data (Real time spectral wave data)
        waveHeight_url = "https://www.ndbc.noaa.gov/data/realtime2/" + self.stn + ".spec"
        request = requests.get(waveHeight_url)
        if not request.status_code == 200:
            print('Buoy link does not exist for %s stn = %s, check station number'%(self.name,self.stn))
            return
        # Save as text file
        urllib.request.urlretrieve(waveHeight_url, self.stn + "_waveHeight.txt")
        specStr = np.genfromtxt(self.stn + "_waveHeight.txt",skip_header=(1),dtype = 'str')
        dateTimeUTC = []
        # Check first and last rows to determine average dt
        timeUnix = np.zeros(2)
        for i in [0,-1]:                               # year              # month          #day            # hour              #min
            dateTimeUTC.append(datetime.datetime(int(specStr[i][0]),int(specStr[i][1]),int(specStr[i][2]),int(specStr[i][3]),int(specStr[i][4]),0))
            timeUnix[i] = calendar.timegm(dateTimeUTC[i].timetuple())
        self.dtSwell = (timeUnix[0]-timeUnix[1])/(len(specStr)-1)
        tEnd = int((daysToLoad*86400*1.2)/(self.dtSwell)) # Find desired start time
        if tEnd > len(specStr):
            print('%i days to load exceeds available data, loading all available data (%i days)...'%(daysToLoad,int((len(specStr)*self.dtSwell)/86400)))
            self.nt = len(specStr)
        else:
            self.nt = tEnd
        self.dateTimeUTC = []
        self.dateTimeLocal = []
        self.timeUnix = np.zeros(self.nt)
        self.WVHT = np.zeros(self.nt) # WVHT
        self.SwH = np.zeros(self.nt)
        self.DPD = np.zeros(self.nt) # SwP
        self.WWH = np.zeros(self.nt)
        self.WWP = np.zeros(self.nt)
        self.SwD = []
        self.WWD = []
        self.APD = np.zeros(self.nt)
        self.MWD = np.zeros(self.nt)
        for i in range(self.nt):                            # year              # month          #day            # hour              #min
            self.dateTimeUTC.append(datetime.datetime(int(specStr[i][0]),int(specStr[i][1]),int(specStr[i][2]),int(specStr[i][3]),int(specStr[i][4]),0))
            self.dateTimeLocal.append(self.dateTimeUTC[i] + datetime.timedelta(seconds=self.localTimeOffset))
            self.timeUnix[i] = calendar.timegm(self.dateTimeUTC[i].timetuple())
            self.WVHT[i] = float(specStr[i][5])
            self.SwH[i] = float(specStr[i][6])
            self.DPD[i] = float(specStr[i][7])
            self.WWH[i] = float(specStr[i][8])
            self.WWP[i] = float(specStr[i][9])
            self.SwD.append(specStr[i][10])
            self.WWD.append(specStr[i][11])
            self.APD[i] = float(specStr[i][13])
            self.MWD[i] = float(specStr[i][14])

        #Pull down the Directional data
        Direction_url = "https://www.ndbc.noaa.gov/data/realtime2/"+ self.stn +".swdir"

        urllib.request.urlretrieve(Direction_url,self.stn +"_dir.txt")
        DirDataStr = np.genfromtxt(self.stn +"_dir.txt",skip_header=(1),dtype = 'str')
        DirData = np.char.strip(DirDataStr,'"()"').astype(float)
        # process time data
        dateTimeSpecUTC = []
        # Check first and last rows to determine average dt
        timeSpecUnix = np.zeros(2)
        for i in [0,-1]:                               # year              # month          #day            # hour              #min
            dateTimeSpecUTC.append(datetime.datetime(int(DirData[i][0]),int(DirData[i][1]),int(DirData[i][2]),int(DirData[i][3]),int(DirData[i][4]),0))
            timeSpecUnix[i] = calendar.timegm(dateTimeSpecUTC[i].timetuple())
        self.dtSpec = (timeSpecUnix[0]-timeSpecUnix[1])/(len(DirData)-1)
        tEndSpec = int((daysToLoad*86400*1.2)/(self.dtSpec)) # Find desired start time
        if tEndSpec > len(DirData):
            print('%i days to load exceeds available data, loading all available data (%i days)...'%(daysToLoad,int((len(DirData)*self.dtSpec)/86400)))
            self.ntSpec = len(DirData)
        else:
            self.ntSpec = tEndSpec
        self.dateTimeSpecUTC = []
        self.dateTimeSpecLocal = []
        self.timeSpecUnix = np.zeros(self.ntSpec)
        for i in range(self.ntSpec):                            # year              # month          #day            # hour              #min
            self.dateTimeSpecUTC.append(datetime.datetime(int(DirData[i][0]),int(DirData[i][1]),int(DirData[i][2]),int(DirData[i][3]),int(DirData[i][4]),0))
            self.dateTimeSpecLocal.append(self.dateTimeSpecUTC[i] + datetime.timedelta(seconds=self.localTimeOffset))
            self.timeSpecUnix[i] = calendar.timegm(self.dateTimeSpecUTC[i].timetuple())
            
            ##
        specDir = DirData[0:self.ntSpec,5::2]
        self.waveFrequency = DirData[0,6::2]
        waveBandwidth = (self.waveFrequency[1:len(self.waveFrequency)]-self.waveFrequency[0:-1])
        self.waveBandwidth = np.append(waveBandwidth,waveBandwidth[-1])
        self.waveMeanDirectionGrid = specDir*(specDir[0]<=360)

        # Pull down the energy data
        Energy_url = "https://www.ndbc.noaa.gov/data/realtime2/"+ self.stn +".data_spec"
        urllib.request.urlretrieve(Energy_url,self.stn +"_spec.txt")
        EngStr = np.genfromtxt(self.stn +"_spec.txt",skip_header=(1),dtype = 'str')
        Eng = np.char.strip(EngStr,'"()"').astype(float)
        waveEnergyDensityGrid = Eng[0:self.ntSpec,6::2]
        
        self.dateTimeLocal = self.dateTimeLocal[::-1]
        self.dateTimeSpecLocal = self.dateTimeSpecLocal[::-1]
        self.dateTimeUTC = self.dateTimeUTC[::-1]
        self.dateTimeSpecUTC = self.dateTimeSpecUTC[::-1]
        self.timeUnix = self.timeUnix[::-1]
        self.timeSpecUnix = self.timeSpecUnix[::-1]
        self.WVHT = np.flip(self.WVHT, axis=0)
        self.SwH = np.flip(self.SwH, axis=0)
        self.DPD = np.flip(self.DPD, axis=0)
        self.APD = np.flip(self.APD, axis=0)
        self.MWD = np.flip(self.MWD, axis=0)
        self.waveEnergyDensityGrid = np.flip(waveEnergyDensityGrid,axis=0)
#         self.waveEnergyDensityGrid = waveEnergyDensityGrid
        
        t1 = time.time()
        total = t1-t0
        print(self.name,"data loaded in %.1f seconds"%total)
        