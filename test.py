from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas

my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
          lat_0=0, lon_0=0)
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'black')
my_map.drawmapboundary()

x,y = my_map(0, 0)
point = my_map.plot(x, y, 'ro', markersize=5)[0]

# Read in the events data.
events = pandas.read_csv("genocide.csv", header=None, dtype=str)
events.columns = ['Event','Geom. mean estimate','From','To','Lat','Long']
#['Event','Location','Geom. mean estimate','Lowest estimate','Highest estimate','From','To','Notes','Lat','Long']


def init():
    point.set_data([], [])
    return point,
    
def grabPoints(year):
    global events
    ans = []
    for name, row in events.iterrows():
        if year in range(int(row["From"]), int(row["To"])+1):
            ans.append(map(float, [row["Long"], row["Lat"], row["Geom. mean estimate"]]))
    return ans

def fetchYears():
    global events
    ans = []
    for name, row in events.iterrows():
        ans += range(int(row["From"]), int(row["To"])+1)
    ans = list(set(ans))
    return sorted(ans)
    
years = fetchYears()
    
# animation function.  This is called sequentially
def animate(i):
    global years
    
    year = years[i]
    points = grabPoints(year)
    print "Year: {}".format(year)
    
    lons = [l[0] for l in points]
    lats = [l[1] for l in points]
    s = [l[2] for l in points]
    x, y = my_map(lons, lats)
    point.set_data(x, y)
    plt.title("Year: {}".format(year))
    #point.set_markersize(s[0])
    return point,

def getRadius(area):
    """Returns the radius of a circle with given area"""
    return math.sqrt(area/math.pi)
    
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=len(years), interval=500, blit=True)

plt.show()