import matplotlib.pyplot as plt
import numpy as np
import pandas
from mpl_toolkits.basemap import Basemap
import locale

# Building base map
my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
          lat_0=0, lon_0=0)
my_map.drawcoastlines()
water = 'black'
my_map.drawcountries()
my_map.fillcontinents(color = 'gray', lake_color=water)
my_map.drawmapboundary(fill_color=water)

# Read in the events data.
try:
    events = pandas.read_csv("data/war.csv", header=None, dtype=str)
except:
    print("File not found!")
events.columns = ['Event','Geom. mean estimate','From','To','Lat','Long']

# Fetches all years that have death records
def fetchYears():
    global events
    ans = []
    for name, row in events.iterrows():
        ans += range(int(row["From"]), int(row["To"])+1)
    ans = list(set(ans))
    return sorted(ans)

# Gets coordinate and death info for a specified year    
def grabPoints(year):
    global events
    ans = []
    for name, row in events.iterrows():
        if year in range(int(row["From"]), int(row["To"])+1):
            ans.append([float(row["Long"]), 
                        float(row["Lat"]), 
                        int(row["Geom. mean estimate"]), 
                        int(row["From"]), 
                        int(row["To"]), 
                        row["Event"]
                       ])
    return ans
    
def getAlphas(points, year):
    """Returns an RGB colour array with alpha values.
    Needed because .scatter() does not accept arrays for the alpha parameter.
    """
    span = [(year - point[3], point[4] + 1 - point[3]) for point in points] # returns duration of events
    alphas = [min(1.0, float(p)/s) for p,s in span]
    numPoints = len(points)
    rgba_colors = np.zeros((numPoints,4))
    # for red the first column needs to be one R,G,B=1,0,0
    rgba_colors[:,0] = 1.0
    # the fourth column needs to be your alphas
    rgba_colors[:, 3] = alphas
    return rgba_colors

# Main loop    
for year in xrange(1900, 2017):
    current = grabPoints(year)
    x = [c[0] for c in current]
    y = [c[1] for c in current]
    x,y = my_map(x,y)
    s = [c[2]/1000 for c in current] # Size of point, is absolute in pixel area
    names = [[c[5], "{:,}".format(c[2])] for c in current] # Event name and death-toll
    alphaColour = getAlphas(current, year)
    
    try:
        fig.remove()
    except:
        pass
    
    fig = my_map.scatter(x, y, s, color=alphaColour, zorder=10)
    plt.title("Year: {}".format(year))
    
    # Plots table - ie event names and death tolls
    try:
        plt.table(colLabels=["Event","Deaths"], 
                  cellText=names,
                  colWidths=[0.1,0.1]
                 ).scale(1,2)
    except:
        pass
    plt.draw()
    
    #plt.savefig('images/{}.png'.format(year))
    
    # Refresh rate
    plt.pause(0.5)
