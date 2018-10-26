import numpy as np
import datetime

# Find nearest value in numpy array
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

# Convert to unix timestamp
def getUnixTimestamp(humanTime,dateFormat):
    unixTimestamp = int(calendar.timegm(datetime.datetime.strptime(humanTime, dateFormat).timetuple()))
    return unixTimestamp

# Convert to human readable timestamp
def getHumanTimestamp(unixTimestamp, dateFormat):
    humanTimestamp = datetime.datetime.utcfromtimestamp(int(unixTimestamp)).strftime(dateFormat)
    return humanTimestamp

def changeDirGap(angle):
#     angleOver180 = angle>=180
    angleUnder180 = angle<=180
    angleUnder180Mod = angleUnder180*360
    angleMod = angle+angleUnder180Mod
    return angleMod

def mapr(radiir):
   """Remap the radial axis."""
   return 0.579998 - radiir

def hourRounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +datetime.timedelta(hours=t.minute//30))

def nextHour(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +datetime.timedelta(hours=1))

def movingAvg(vector,N):
    cumsum, moving_aves = [0], []
    for i, x in enumerate(vector, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves