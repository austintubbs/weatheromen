import numpy as np
import time

class buoy:
   # """Represents a wave buoy, with a name."""
    # A class variable, counting the stn of buoys
    def __init__(self,name,stn,localTimeOffset):  #Name, Station stn, and Local Time Offset in Hours
        """Initializes the data."""
        self.name = name
        self.stn = str(stn)
        self.localTimeOffset = localTimeOffset*3600
#         print("(Initializing {} {})".format(self.name,self.stn))
        # When this buoy is created, the buoy
        # adds to the population
    
    def calcWaveHeight(self):
        t0 = time.time()
        self.Sep_Freq = 9.999
        self.wavePeriod = 1/self.waveFrequency
        self.swellBands = self.waveFrequency<1/self.Sep_Freq
        self.swellFrequency = self.waveFrequency[self.swellBands]
        self.swellBandwidth = self.waveBandwidth[self.swellBands]
        n = self.nt
        m = len(self.waveEnergyDensityGrid[0])
        lenSBW = sum(self.swellBands)
        self.waveEnergyDensity = np.zeros([n,m],dtype=np.float)
        self.swellEnergyDensity = np.zeros([n,lenSBW],dtype=np.float)
        m0 = np.zeros(n,dtype=np.float)
        swellm0 = np.zeros(n,dtype=np.float)
        self.MWH = np.zeros(n,dtype=np.float)
        self.WVHT = np.zeros(n,dtype=np.float)
        self.SwH = np.zeros(n,dtype=np.float)
        self.RMSWH = np.zeros(n,dtype=np.float)
        for i in range(n):
        #     print(waveEnergyDensityGrid[i])
            self.waveEnergyDensity[i] = self.waveEnergyDensityGrid[i]
            self.swellEnergyDensity[i] = self.waveEnergyDensity[i][self.swellBands]
            m0[i] = sum(self.waveEnergyDensity[i]*self.waveBandwidth)
            swellm0[i] =  sum(self.swellEnergyDensity[i]*self.swellBandwidth)
            self.MWH[i] = np.sqrt(2*np.pi*m0[i]) #*3.28084
            self.WVHT[i] = 4*np.sqrt(m0[i]) #*3.28084
            self.SwH[i] = 4*np.sqrt(swellm0[i]) #*3.28084
            self.RMSWH[i] = np.sqrt(8*m0[i]) #*3.28084

        self.maxEnergyID = np.unravel_index(np.argmax(self.waveEnergyDensityDirectionGrid, axis=None), self.waveEnergyDensityDirectionGrid.shape)

        ###### 9 band #######
        m0grid = self.waveEnergyDensityGrid*self.waveBandwidth
        # WVHTgrid = 1/2*np.sqrt(m0grid)
        nineBandIDs = np.array([[0,3],[4,5],[6,7],[8,9],[10,11],[12,14],[15,17],[18,21],[22,63]])
        nineBandEnergy = np.zeros([self.nt,len(nineBandIDs)])
        for j in range(self.nt):
            for i in range(len(nineBandIDs)):
                nineBandEnergy[j][i]=np.sum(m0grid[j,nineBandIDs[i,0]:nineBandIDs[i,1]])
        self.nineBandWVHT = 4*np.sqrt(nineBandEnergy)

        nDir = np.shape(self.waveMeanDirectionGrid)[0]
        nineBandDirection = np.zeros([nDir,len(nineBandIDs)])
        for j in range(nDir):
            for i in range(len(nineBandIDs)):
                nineBandDirection[j][i]=np.mean(self.waveMeanDirectionGrid[j,nineBandIDs[i,0]:nineBandIDs[i,1]])
        self.nineBandDirection = nineBandDirection
        t1 = time.time()
        total = t1-t0
        print(self.name,"wave heights calculated in %.1f seconds"%total)
        
    def findSwells(self,neighborhood_size,thresholdDivisor):
        nSwells = 5 #np.size(x)
        self.swellEnergy = np.zeros((self.nt,nSwells))
        self.swellHeight = np.zeros((self.nt,nSwells))
        self.swellPeriod = np.zeros((self.nt,nSwells))
        self.swellDirection = np.zeros((self.nt,nSwells))
        for l in range(self.nt):
            maxEnergy=np.max(self.waveEnergyDensityDirectionGrid[l,:,:])
            n = np.floor(255/maxEnergy)
            energyPixels = (n*self.waveEnergyDensityDirectionGrid[l,:,:]).astype(int)
            # energyPixels
            ###### PEAK DETECTION
            neighborhood_size = 3
            neighborhood = [[0,1,0],[1,1,1],[0,1,0]]
            threshold = 255/thresholdDivisor
            useFootprint = 0
            data = Image.fromarray(energyPixels)
            if useFootprint:
                data_max = filters.maximum_filter(data,footprint=neighborhood)
                data_min = filters.minimum_filter(data, footprint=neighborhood)
            else:
                data_max = filters.maximum_filter(data,neighborhood_size)
                data_min = filters.minimum_filter(data, neighborhood_size)

            maxima = (energyPixels == data_max)
            diff = ((data_max - data_min) > threshold)
            maxima[diff == 0] = 0

            labeled, num_objects = ndimage.label(maxima)
            slices = ndimage.find_objects(labeled)
            x, y = [], []
            for dy,dx in slices:

                x_center = int((dx.start + dx.stop - 1)/2)
                x.append(x_center)
                y_center = int((dy.start + dy.stop - 1)/2)    
                y.append(y_center)

            nSwellsFound = np.size(x)
            freqMax = np.shape(self.waveEnergyDensityDirectionGrid[l,:,:])[0]-1
            freqMin = 0
            dirMin = 0
            dirMax = np.shape(self.waveEnergyDensityDirectionGrid[l,:,:])[1]-1
            nFreqsPerBin = 5
            nDirsPerBin = 5
            freq0 =int((nFreqsPerBin-1)/2)
            dir0 =int((nDirsPerBin-1)/2)
            for k in range(nSwellsFound):
                for i in range(-dir0,dir0+1):
            #         print(i)
                    for j in range(-freq0,freq0+1):
            #             print(j)
                        freqID = int(y[k])+j
                        dirID = int(x[k])+i
                        if freqID < freqMin:
                            break
                        elif freqID > freqMax:
                            break
                        if dirID < dirMin:
                            break
                        elif dirID > dirMax:
                            break
            #             print(dirID,freqID)
#                         print(nSwells,nSwellsFound,x)
                        if k>nSwellsFound:
                            self.swellEnergy[l,k] = 0
                        else:
                            self.swellEnergy[l,k] = self.swellEnergy[l,k]+ self.waveEnergyDensityDirectionGrid[l,freqID,dirID]*5*self.waveBandwidth[freqID]
                self.swellHeight[l,k] = 3.28*4*np.sqrt(self.swellEnergy[l,k])
                self.swellPeriod[l,k] = self.wavePeriod[int(y[k])]
                self.swellDirection[l,k] = self.waveDirection[int(x[k])]
                print("Swell %i = %.1f feet at %.1f seconds from %.1f degrees"%(k+1,self.swellHeight[l,k],self.swellPeriod[l,k],self.swellDirection[l,k]))