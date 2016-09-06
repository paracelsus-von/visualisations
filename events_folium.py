import folium
from folium import plugins
import random
import pandas
import math

# Read in the events data.
events = pandas.read_csv("data/genocide.csv", header=None, dtype=str)
events.columns = ['Event','Geom. mean estimate','From','To','Lat','Long']
#['Event','Location','Geom. mean estimate','Lowest estimate','Highest estimate','From','To','Notes','Lat','Long']

#Constants
start = min(events["From"])
end = 2016

def getRadius(area):
    """Returns the radius of a circle with area"""
    return math.sqrt(area/math.pi)

# Get a basic world map.
events_map = folium.Map(location=[30, 0], zoom_start=2)

# Draw markers on the map.
def generateMap(year):
    global events
    events_map = folium.Map(location=[30, 0], zoom_start=2)
    for name, row in events.iterrows():
        try:
            assert(year == row["From"])
            deaths = int(row["Geom. mean estimate"])
            folium.CircleMarker([row["Lat"], row["Long"]], 
                                 popup=row["Event"] + ": {:,}".format(deaths),
                                 radius=getRadius(deaths)*1000
                               ).add_to(events_map)
        except:
            continue
        # Create and show the map.
        events_map.save('maps\events_' + str(year) + '.html')
        
#for year in events["From"]:
#    generateMap(year)

from ipywidgets import StaticInteract, RangeWidget, RadioWidget

StaticInteract(generateMap, year=Rangewidget(1900,2017,1)