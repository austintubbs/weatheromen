from buoy import buoy
import datetime
import numpy as np
import buoyUtils
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import (HOURLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

def forecast(wBuoy,hBuoy,buoy1):

    buoyDist = 505966.4 # meters = 273.2 nautical miles
    buoyDir = 308
    swellDirRange = [270,45]
    b1offset = buoy("Buoy 1 Offset",51001,-10) # Create fake buoy with offset data
    [b1offset.dateTimeLocal,b1offset.SwH,b1offset.DPD,b1offset.MWD] = calcSwellOffset(buoy1,buoyDist,buoyDir,swellDirRange)

    buoyDist = 165198.4 # meters = 89.2 nautical miles
    buoyDir = 295
    swellDirRange = [270,45]
    hBoffset = buoy("Hanalei Buoy Offset",202,-10) # Create fake buoy with offset data
    [hBoffset.dateTimeLocal,hBoffset.SwH,hBoffset.DPD,hBoffset.MWD] = calcSwellOffset(hBuoy,buoyDist,buoyDir,swellDirRange)
    
    plot(wBuoy,hBuoy,hBoffset,buoy1,b1offset)
    x=1

def plot(wBuoy,hBuoy,hBoffset,buoy1,b1offset):
    # Day and hour locator for plots
    days = mdates.DayLocator()   # every day
    hours = mdates.HourLocator()  # every hour
    dateFmt = mdates.DateFormatter('%H:%M\n%m/%d')
    rule = rrulewrapper(HOURLY, interval=3)
    loc = RRuleLocator(rule)
    # Change location of direction gap so its not at 360 degrees
    wBuoyWaveDpMod = buoyUtils.changeDirGap(wBuoy.MWD)
    hBuoyWaveDpMod = buoyUtils.changeDirGap(hBuoy.MWD)
    b1offsetWaveDpMod = buoyUtils.changeDirGap(b1offset.MWD)
    hBoffsetWaveDpMod = buoyUtils.changeDirGap(hBoffset.MWD)
    # Set direction plot limits
    dirStart = 270
    dirEnd = 45
    dirDt = 15
    directionLabels = np.concatenate((np.arange(dirStart,360+dirDt,dirDt),np.arange(dirDt,dirEnd+dirDt,dirDt)))

    dateMin = buoyUtils.hourRounder(wBuoy.dateTimeLocal[0])
    dateMax = buoyUtils.nextHour(b1offset.dateTimeLocal[0])
    
    fig, ax = plt.subplots(3,1,figsize=[15,15])
    for i in range(3):
        ax[i].grid(True, ls=":")
        # format the ticks
        ax[i].xaxis.set_major_locator(loc)
        ax[i].xaxis.set_major_formatter(dateFmt)
        ax[i].xaxis.set_minor_locator(hours)
        ax[i].set_xlim(dateMin, dateMax)
#         ax[i].set_xlim(datetime.date(2018,10,15),datetime.date(2018,10,17))
        #ax[i].set_xlabel("Date")
    ax[0].set_ylabel("Wave Height [ft]")
    ax[1].set_ylabel("Wave Period [sec]")
    # Direction
    ax[2].set_ylim([0,360])
    ax[2].set_ylabel("Wave Direction [°]")
    ax[2].set_ylim([dirStart,dirEnd+360])
    ax[2].set_yticks(np.arange(dirStart,dirEnd+dirDt+360,dirDt))
    ax[2].set_yticklabels(directionLabels)
    # Spectrum
#     ax[3].set_ylabel("Energy [$\mathregular{m^2/Hz}}$]")
#     ax[3].set_xlabel("Period [s]")
#     ax[3].grid(True, ls=":")
#     ax[3].set_xlim([6,22])

    ax[0].plot(wBuoy.dateTimeLocal,wBuoy.SwH[0:wBuoy.nt]*3.28084,'.-',label="Waimea Swell Height")
#     ax[0].plot(hBuoy.dateTimeLocal,hBuoy.SwH[0:hBuoy.nt]*3.28084,'.-',label="Hanalei Swell Height")
#     ax[0].plot(buoy1.dateTimeLocal,buoy1.SwH*3.28084,'.-',label="Buoy 1 Swell Height")
    ax[0].plot(b1offset.dateTimeLocal,b1offset.SwH*3.28084,'.-',label="Buoy 1 Offset Swell Height")
    ax[0].plot(hBoffset.dateTimeLocal,hBoffset.SwH*3.28084,'.-',label="Hanalei Offset Swell Height")
#     ax[0].plot(wBuoy.dateTimeLocal,wBuoy.WVHT[startDateID:wBuoy.nt]*3.28084,'.-',label="Wave Height")
#     ax[0].plot(wBuoy.dateTimeLocal,wBuoy.waveHs[startDateID:wBuoy.nt]*3.28084,'.-',label="Wave Height (check)")
    ax[1].plot(wBuoy.dateTimeLocal,wBuoy.DPD[0:wBuoy.nt],'.-',label="Waimea Swell Period")
#     ax[1].plot(hBuoy.dateTimeLocal,hBuoy.DPD[0:hBuoy.nt],'.-',label="Hanalei Swell Period")
    ax[1].plot(b1offset.dateTimeLocal,b1offset.DPD,'.-',label="Buoy 1 Offset Swell Period")
    ax[1].plot(hBoffset.dateTimeLocal,hBoffset.DPD,'.-',label="Hanalei Offset Swell Period")
#     ax[1].plot(wBuoy.dateTimeLocal,self.waveTa[startDateID:self.nt],'.-',label="Average Wave period")
    ax[2].plot(wBuoy.dateTimeLocal,wBuoyWaveDpMod[0:wBuoy.nt],'.-',label="Waimea Swell Direction")
#     ax[2].plot(hBuoy.dateTimeLocal,hBuoyWaveDpMod[0:hBuoy.nt],'.-',label="Hanalei Swell Direction") 
    ax[2].plot(b1offset.dateTimeLocal,b1offsetWaveDpMod,'.-',label="Buoy 1 Offset Swell Direction")
    ax[2].plot(hBoffset.dateTimeLocal,hBoffsetWaveDpMod,'.-',label="Hanalei Offset Swell Direction")
#     ax[3].plot(self.wavePeriod,self.waveEnergyDensity[-1],'.-')

    for i in range(3):
        ax[i].legend(fontsize=12, loc=2, facecolor="white")
    plt.title("Oahu Short Term Wave Forecast", fontsize=18, y=3.4)

#     fig.text(0.3,0.89,"WVHT = "+str(round(wBuoy.WVHT[-1]*3.28084,2))+" ft    "+
#              "SwH = "+str(round(wBuoy.SwH[-1]*3.28084,2))+" ft    "+
#              "Period = "+str(round(wBuoy.DPD[-1],1))+" seconds    "+
#              "Direction = "+str(round(wBuoy.MWD[-1],1))+" deg    "+
#              str(wBuoy.dateTimeLocal[-1]))
    fig.savefig('figures/Oahu Forecast.png')
    
    
def calcSwellOffset(self,buoyDist,buoyDir,swellDirRange):
# self = buoy object from which to calculate swell height at a point of interest
# buoyDist = distance between the buoy and point of interest
# buoyDir = compass direction of buoy from point of interest
# swellDirRange = 2 object list of direction window moving clockwise
#     self.MWD = self.waveDp
#     self.DPD = self.waveTp
    u = 7.0*10**(-7) # decay rate
    direction=np.zeros(self.nt)
    period=np.zeros(self.nt)
    swellHeight=np.zeros(self.nt)
    distance = np.zeros(self.nt)
    time1Local = []
    count = 0
    for i in range(self.nt):
        if swellDirRange[0] <= self.MWD[i] <= swellDirRange[1] + 360:
            direction[count] = self.MWD[i]
            distance[count] = buoyDist * np.cos(np.pi*abs(direction[count]-buoyDir)/180)
            period[count] = self.DPD[i]
            swellHeight[count] = self.SwH[i] * np.exp(-u*distance[count])
#             print(self.SwH[i] * np.exp(-u*distance[count]))
            time1Local.append(self.dateTimeLocal[i])
            count = count+1
    direction = direction[0:count]
    period=period[0:count]
    swellHeight=swellHeight[0:count]
    distance = distance[0:count]
     
    
    g = 9.80665
    waveLength = (g*period**2)/(2*np.pi)
    waveSpeed = waveLength/period
    groupVelocity = waveSpeed/2
    timeDelta = distance/groupVelocity
    time2Local = []
    for i in range(len(time1Local)):
        time2Local.append(time1Local[i] + datetime.timedelta(seconds=timeDelta[i]))
    # Sort new data
    sortedIDs = sorted(range(len(time2Local)), key=lambda k: time2Local[k], reverse=True)
    time2Local = sorted(time2Local, reverse=True)
    swellHeight = swellHeight[sortedIDs]
    period = period[sortedIDs]
    direction = direction[sortedIDs]
#     swellHeightFilt = buoyUtils.movingAvg(swellHeight,3)
    return time2Local,swellHeight,period,direction