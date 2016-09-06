import pandas
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
plt.ion()

t=0
r=3.0
n=0

my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
          lat_0=0, lon_0=0)
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'black')
my_map.drawmapboundary()


# Read in the events data.
events = pandas.read_csv("genocide.csv", header=None, dtype=str)
events.columns = ['Event','Geom. mean estimate','From','To','Lat','Long']
#['Event','Location','Geom. mean estimate','Lowest estimate','Highest estimate','From','To','Notes','Lat','Long']


def fetchYears():
    global events
    ans = []
    for name, row in events.iterrows():
        ans += range(int(row["From"]), int(row["To"])+1)
    ans = list(set(ans))
    return sorted(ans)

def grabPoints(year):
    global events
    ans = []
    for name, row in events.iterrows():
        if year in range(int(row["From"]), int(row["To"])+1):
            ans.append(map(float, [row["Long"], row["Lat"], row["Geom. mean estimate"]]))
    return ans
    
years = fetchYears()

for m in range(len(events)):
    plt.draw()
plt.pause(1)

for year in years:
    A = grabPoints(year)
    x,y = my_map([a[0] for a in A], [a[1] for a in A])
    plt.scatter(x, y, marker="o", color="red", s = [a[2]/1000 for a in A])
    plt.title("Year: {}".format(year))
    plt.draw()
    plt.pause(1)
  