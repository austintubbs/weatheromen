import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import (HOURLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import buoyUtils
import datetime

def plotNineBands(self):
    # Day and hour locator for plots
    days = mdates.DayLocator()   # every day
    hours = mdates.HourLocator()  # every hour
    dateFmt = mdates.DateFormatter('%H:%M\n%m/%d')
    rule = rrulewrapper(HOURLY, interval=3)
    loc = RRuleLocator(rule)
    # Change location of direction gap so its not at 360 degrees
    nT, nBands = np.shape(self.nineBandDirection)
    nineBandDirectionMod = np.zeros((nT,nBands))
    for i in range(nBands):
        nineBandDirectionMod[:,i] = buoyUtils.changeDirGap(self.nineBandDirection[:,i])
    # Set direction plot limits
    dirStart = 180
    dirEnd = 180
    dirDt = 30
    directionLabels = np.concatenate((np.arange(dirStart,360+dirDt,dirDt),np.arange(dirDt,dirEnd+dirDt,dirDt)))

    dateMin = buoyUtils.hourRounder(self.dateTimeLocal[0])
    dateMax = buoyUtils.nextHour(self.dateTimeLocal[-1])
    
    # Create figure
    fig, ax = plt.subplots(2,1,figsize=[15,10])
    for i in range(2):
        ax[i].grid(True, ls=":")
        # format the ticks
        ax[i].xaxis.set_major_locator(loc)
        ax[i].xaxis.set_major_formatter(dateFmt)
        ax[i].xaxis.set_minor_locator(hours)
        ax[i].set_xlim(dateMin, dateMax)
    ax[1].set_ylim([dirStart,dirEnd+360])
    ax[1].set_yticks(np.arange(dirStart,dirEnd+dirDt+360,dirDt))
    ax[1].set_yticklabels(directionLabels)
    ax[0].set_ylabel("Wave Height [ft]")
    ax[1].set_ylabel("Wave Direction [°]")

#         # Direction
#         ax[2].set_ylim([0,360])
#         ax[2].set_ylabel("Wave Direction [°]")

    labelArray = ["22+ sec","22-18 sec","18-16 sec","16-14 sec","14-12 sec","12-10 sec","10-8 sec","8-6 sec","under 6 sec"]
    ax[0].plot(self.dateTimeLocal,self.nineBandWVHT[0:self.nt]*3.28084,)#,label=labelArray)
#         plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d% %H:%M'))
#         plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    ax[1].plot(self.dateTimeLocal,nineBandDirectionMod[0:self.nt]) #,'.-',label="Wave Height")
#         plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d% %H:%M'))
#         plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    ax[0].legend(labelArray, loc=2, facecolor="white")
    ax[1].legend(labelArray, loc=2, facecolor="white")
    plt.title("9-Band Wave Heights and Directions for "+self.name, fontsize=18, y=2.2)
    fig.savefig("figures/%s 9band.png"%self.name)

def heightPerDir(self):
    # Day and hour locator for plots
    days = mdates.DayLocator()   # every day
    hours = mdates.HourLocator()  # every hour
    dateFmt = mdates.DateFormatter('%H:%M\n%m/%d')
    rule = rrulewrapper(HOURLY, interval=3)
    loc = RRuleLocator(rule)
    # Change location of direction gap so its not at 360 degrees
    MWDMod = buoyUtils.changeDirGap(self.MWD)
    # Set direction plot limits
    dirStart = 270
    dirEnd = 45
    dirDt = 15
    directionLabels = np.concatenate((np.arange(dirStart,360+dirDt,dirDt),np.arange(dirDt,dirEnd+dirDt,dirDt)))

    dateMin = buoyUtils.hourRounder(self.dateTimeLocal[0])
    dateMax = buoyUtils.nextHour(self.dateTimeLocal[-1])
    
    # Create the figure
    fig, ax = plt.subplots(4,1,figsize=[15,20])
    # Format the x-axis
    for i in range(3):
        ax[i].grid(True, ls=":")
        # format the ticks
        ax[i].xaxis.set_major_locator(loc)
        ax[i].xaxis.set_major_formatter(dateFmt)
        ax[i].xaxis.set_minor_locator(hours)
        ax[i].set_xlim(dateMin, dateMax)
        #ax[i].set_xlabel("Date")
    
    # Set specific axis values
    ax[0].set_ylabel("Wave Height (ft)")
    ax[1].set_ylabel("Wave Period (sec)")
    # Direction
    ax[2].set_xlim([self.dateTimeLocal[0],self.dateTimeLocal[-1]])
    ax[2].set_ylim([dirStart,dirEnd+360])
    ax[2].set_yticks(np.arange(dirStart,dirEnd+dirDt+360,dirDt))
    ax[2].set_yticklabels(directionLabels)
    ax[2].set_ylabel("Wave Direction (°)")
    # Spectrum
    ax[3].set_ylabel("Energy ($\mathregular{m^2/Hz}}$)")
    ax[3].set_xlabel("Period (s)")
    ax[3].grid(True, ls=":")
    ax[3].set_xlim([6,22])
    # Shadow boxes
    #     ax[2].axhspan(272, 292, alpha=0.5, color='red')
    #     ax[i].axvspan(self.dateTimeLocal[-1], self.dateTimeLocal[-5], alpha=0.5, color='grey')

    # Plot lines
    ax[0].plot(self.dateTimeLocal,self.SwH[0:self.nt]*3.28084,'.-',label="Swell Height")
    ax[0].plot(self.dateTimeLocal,self.WVHT[0:self.nt]*3.28084,'.-',label="Wave Height")
    ax[0].plot(self.dateTimeLocal,self.waveHs[0:self.nt]*3.28084,'.-',label="Wave Height (check)")
    ax[1].plot(self.dateTimeLocal,self.DPD[0:self.nt],'.-',label="Peak Wave Period")
    ax[1].plot(self.dateTimeLocal,self.waveTa[0:self.nt],'.-',label="Average Wave period")
    ax[2].plot(self.dateTimeLocal,MWDMod[0:self.nt],'.-')#,label="Peak Wave Direction")
    ax[3].plot(self.wavePeriod,self.waveEnergyDensity[-1],'.-')
    # Insert legends
    for i in range(2):
        ax[i].legend(fontsize=12, loc=2, facecolor="white")
        
#     print("SWVHT = "+str(round(self.waveHs[-1]*3.28084,2))+" ft at "+str(round(self.DPD[-1],1))+" seconds")
#     print("WVHT = "+str(round(self.WVHT[-1]*3.28084,2))+" ft at "+str(round(self.DPD[-1],1))+" seconds")
#     print("SwH = "+str(round(self.SwH[-1]*3.28084,2))+" ft at "+str(round(self.DPD[-1],1))+" seconds")
#     print("Dir = "+str(round(self.MWD[-1],2))+" degrees")
#     print(self.dateTimeLocal[-1])

    fig.text(0.3,0.89,"WVHT = "+str(round(self.WVHT[-1]*3.28084,2))+" ft    "+
             "SwH = "+str(round(self.SwH[-1]*3.28084,2))+" ft    "+
             "Period = "+str(round(self.DPD[-1],1))+" seconds    "+
             "Direction = "+str(round(self.MWD[-1],1))+" deg    "+
             str(self.dateTimeLocal[-1]))
    #          plt.title("Recent Wave data for "+self.name, fontsize=18, y=8)
    fig.savefig("figures/%s heightPerDir.png"%self.name)
   
def polarHeatMap(self):
    # define axes:
    z=self.waveEnergyDensityDirectionGrid[-1]
    y=1/self.frequencyBins
    x= np.pi * self.directionBins / 180 #convert to radian
    # Set the degree grid
    degSpacing = 10
    degrange = range(0,360,degSpacing)
    # Set the period min, max and grid
    ylabels = [20,18,16,14,12,10,8,6]
    yMin = 6
    yMax = 22
    # Modify the "jet" colormap to make the bottom color white
    colormap = plt.cm.jet(np.linspace(0, 1, 256))
    colormap[0,0:3] = [1,1,1]
    colormap
    # generating a smoothly-varying LinearSegmentedColormap
    cmap = colors.LinearSegmentedColormap.from_list('colormap', colormap)

    # Setup figure
    fig2 = plt.figure(figsize=(11,11))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")
    lines, labels = plt.thetagrids(degrange, labels=None)#, frac = 1.07)
    ax.set_ylim(yMin,yMax)
    ax.set_yticks(ylabels)
    ax.set_yticklabels(ylabels)
    # Plot the colormesh
    colorax = ax.pcolormesh(x,y, z,cmap=cmap, norm=colors.LogNorm(vmin=0.0001, vmax=z.max()))
    # Plot the grid
    plt.grid()
    # Create the colorbar
    cbar = fig2.colorbar(colorax)
    cbar.set_label("Energy Density [m^2/Hz/°]", rotation=270, fontsize=16, labelpad=30) # label pad is the x offset
    
    plt.suptitle('Wave Buoy Spectrum for '+self.name, fontsize=22, y=0.95, x=0.44)
    dateLabel = self.dateTimeLocal[-1].strftime('%m/%d/%Y %H:%M')  
    plt.title(dateLabel+" HST", fontsize=22, y=1.11)
    fig2.text(0.08,0.8,"WVHT = "+str(round(self.WVHT[-1]*3.28084,2))+" ft\nSwH = "+str(round(self.SwH[-1]*3.28084,2))+
             " ft\nPeriod = "+str(round(self.DPD[-1],1))+" s\nDirection = "+str(round(self.MWD[-1],1))+"°")
    # Save the plot
    fig2.savefig("figures/%s polarHeatMap.png"%self.name)