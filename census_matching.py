import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df = pd.read_pickle("pickled_madrid_orders.pkl")
df = df.dropna()
gdf = gpd.read_file("../GEOSPATIAL/cartografia_censo2011_nacional/SECC_CPV_E_20111101_01_R_INE.shp")
gdf_madrid = gdf.loc[gdf['NPRO']=="Madrid"]

dict_cusec={cusec:0 for cusec in gdf_madrid['CUSEC'].unique()}
#test

df = df.sample(100)


for index in df.index:
    print(index)
    lat, lng = df.loc[index,'LAT'], df.loc[index, 'LNG']
    print(lng, lat)
    p = Point(lat,lng)
    print(p)
    for ix2 in gdf_madrid.index:
        print(gdf_madrid.loc[ix2,'geometry'].centroid)
        if gdf_madrid.loc[ix2,'geometry'].contains(p):
            print("FOUND ",gdf_madrid.loc[ix2, 'CUSEC'])
            print()
            dict_cusec[gdf_madrid.loc[ix2, 'CUSEC']]+=1



# sorted = gdf_madrid.sort(columns=['COUNT'], ascending=False)
# print(sorted.head(30))