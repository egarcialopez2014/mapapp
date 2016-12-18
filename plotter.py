import pandas as pd
import numpy as np
from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt
from collections import namedtuple
import json
import mplleaflet

def geo_point(point):
    geoPoint = {"type": "Feature", "geometry":{"type": "Point", "coordinates":[]},"properties":{}}
    geoPoint["geometry"]["coordinates"]=[point.lng, point.lat]
    properties = {"order":point.order_id, "order_date":point.order_date, "value":point.order_value, "address":point.full_address}
    geoPoint["properties"]=properties
    return geoPoint

def geo_features(list_of_points):
    feature_collection = {"type": "FeatureCollection", "features":[geo_point(point) for point in list_of_points]}
    return feature_collection


app = Flask(__name__)

df_work = pd.read_pickle("pickled_orders.pkl")
df_madrid = pd.read_pickle("pickled_madrid_orders.pkl")
print("All good - loaded pickles")
Point = namedtuple('Point', ['order_id', 'order_date','full_address','order_value','lat', 'lng'])
all_points = []
madrid_points = []
for idx, row in df_work.iterrows():
    all_points.append(Point._make(row))
for idx, row in df_madrid.iterrows():
    madrid_points.append(Point._make(row))
featured_points = geo_features(all_points)
madrid_points = geo_features(madrid_points)


@app.route("/")
def home():
    return render_template("order_locator.html", geo_features = featured_points)

@app.route("/census")
def with_census():
    return render_template("order_locator_census.html", geo_features = featured_points)

@app.route("/madrid")
def only_madrid():
    return render_template("order_locator.html", geo_features = madrid_points)

@app.route("/heatmap")
def madrid_heatmap():
    return render_template("order_locator_heatmap.html", geo_features = madrid_points)



if __name__ == '__main__':
    app.run(port=5000, debug=True)





#df_work_2=df_work.dropna()
#plt.scatter(df_work_2['LNG'], df_work_2['LAT'])

#tengo que sacar el url directamente de MapBox
#probar tambien con Bokeh!

#tile_URL = "https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?"
#access_token = "pk.eyJ1IjoiZWdhcmNpYWxvcGV6IiwiYSI6ImhtOTB1cHcifQ.X36jmPbivQRGhgAh02oc-A"

#mplleaflet.show()

