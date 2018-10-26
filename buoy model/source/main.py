from NOAAbuoy import NOAAbuoy
from CDIPbuoy import CDIPbuoy 
import buoyPlots
import oahuForecast

# from importlib import reload
# import NOAAbuoy
# reload(NOAAbuoy)
# from NOAAbuoy import NOAAbuoy
# import CDIPbuoy
# reload(CDIPbuoy)
# from CDIPbuoy import CDIPbuoy
# import buoy
# reload(buoy)
# from buoy import buoy
# reload(buoyPlots)

# How many days of data to plot backwards in time
plotTimeDays = 2

# Initialize Buoys
wBuoy = CDIPbuoy("Waimea Buoy CDIP",106,-10) #Name, Station Number, and Local Time Offset in Hours
hBuoy = CDIPbuoy("Hanalei Buoy CDIP",202,-10) #Name, Station Number, and Local Time Offset in Hours
buoy1 = NOAAbuoy("Buoy 1 NOAA",51001,-10) #Name, Station Number, and Local Time Offset in Hours
hBuoy2 = NOAAbuoy("Hanalei Buoy NOAA",51208,-10) #Name, Station Number, and Local Time Offset in Hours

# Load data and calculate wave heights
wBuoy.loadNetCDF(plotTimeDays)
wBuoy.calcWaveHeight()
hBuoy.loadNetCDF(plotTimeDays)
hBuoy.calcWaveHeight()
buoy1.loadData(plotTimeDays)
buoy1.calcWaveHeight()
hBuoy2.loadData(plotTimeDays)
hBuoy2.calcWaveHeight()

# Make buoy plots
buoyPlots.heightPerDir(wBuoy)
buoyPlots.polarHeatMap(wBuoy)
buoyPlots.plotNineBands(wBuoy)

buoyPlots.heightPerDir(hBuoy)
buoyPlots.polarHeatMap(hBuoy)
buoyPlots.plotNineBands(hBuoy)

oahuForecast.forecast(wBuoy,hBuoy,buoy1)
# buoyPlots.compare(hBuoy,hBuoy2)