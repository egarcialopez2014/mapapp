import pandas as pd
import numpy as np
import requests
import googlemaps


def geo_encoding(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    url = base_url+address.replace(" ","+")+'&key='+google_key
    r=requests.get(url)
    if r.json()['status'] == "OK":
        lat = r.json()['results'][0]['geometry']['location']['lat']
        lng = r.json()['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return np.NaN, np.NaN

print("loading DF")
path = "/Users/egarcialopez/Desktop"
filename = path + "/Info_Pedidos_Online.csv"
google_key = 'AIzaSyA4EvoAVRjsHDdpOqiUu0zBV2tI8vesy0M'

gmaps = googlemaps.Client(key=google_key)

df = pd.read_csv(filepath_or_buffer=filename, sep=None, parse_dates=[1,2], decimal=",")
df['full_address']=df['TIPO_VIA']+' '+df['ADDRESS_1']+' '+df['ADDRESS_2']+', '+df['CITY']+', '+df['PROVINCIA']
df_Madrid = df[df['PROVINCIA']=="MADRID"]
df_work = df_Madrid.sample(2000)[['ORDER_ID','SUBMITTED_DATE','full_address','IMPORTE_WEB']].dropna()



# Add columns to DF with Lat, Lng and fill with lat, lng

print("extending with lat, long")

df_work['LAT']=''
df_work['LNG']=''

for index in df_work.index:
    lat, lng = geo_encoding(df_work.loc[index,'full_address'])
    df_work.loc[index, 'LAT'] = lat
    df_work.loc[index, 'LNG'] = lng

print("DONE ENCODING")

df_work.to_pickle("pickled_madrid_orders.pkl")

# Pass onto map


