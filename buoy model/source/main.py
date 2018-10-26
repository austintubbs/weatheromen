from CDIPbuoy import CDIPbuoy 
from NOAAbuoy import NOAAbuoy
# from buoy import buoy 
import buoyPlots
import oahuForecast
# How many days of data to plot backwards in time
plotTimeDays = 2

# Initialize Buoys
wBuoy = CDIPbuoy("Waimea Buoy",106,-10) #Name, Station Number, and Local Time Offset in Hours
hBuoy = CDIPbuoy("Hanalei Buoy",202,-10) #Name, Station Number, and Local Time Offset in Hours
buoy1 = NOAAbuoy("Buoy 1",51001,-10) #Name, Station Number, and Local Time Offset in Hours
# Load data and calculate wave heights
wBuoy.loadNetCDF(plotTimeDays)
wBuoy.calcWaveHeight()
hBuoy.loadNetCDF(plotTimeDays)
hBuoy.calcWaveHeight()
buoy1.loadData(plotTimeDays)

# Make buoy plots
buoyPlots.heightPerDir(wBuoy)
buoyPlots.polarHeatMap(wBuoy)
buoyPlots.plotNineBands(wBuoy)

buoyPlots.heightPerDir(hBuoy)
buoyPlots.polarHeatMap(hBuoy)
buoyPlots.plotNineBands(hBuoy)

oahuForecast.forecast(wBuoy,hBuoy,buoy1)
