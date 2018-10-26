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
        urllib.request.urlretrieve(waveHeight_url, self.stn + "_waveHeight.txt")
        specStr = np.genfromtxt(self.stn + "_waveHeight.txt",skip_header=(1),dtype = 'str')
        dateTimeUTC = []
        timeUnix = np.zeros(2)
        for i in range(2):                                # year              # month          #day            # hour              #min
            dateTimeUTC.append(datetime.datetime(int(specStr[i][0]),int(specStr[i][1]),int(specStr[i][2]),int(specStr[i][3]),int(specStr[i][4]),0))
            timeUnix[i] = calendar.timegm(dateTimeUTC[i].timetuple())
        self.dtSwell = timeUnix[0]-timeUnix[1]
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

        t1 = time.time()
        total = t1-t0
        print(self.name,"data loaded in %.1f seconds"%total)