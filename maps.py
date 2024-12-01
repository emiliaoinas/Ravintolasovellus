import psycopg2
import pandas as pd
import geopandas as gpd
import folium
from db import db
from sqlalchemy.sql import text
from shapely.geometry import Point

def create_map():
    sql = text("SELECT id, restaurant_name, latitude, longitude FROM restaurants")
    result = db.session.execute(sql)
    rows = result.fetchall()

    columns = result.keys()
    df = pd.DataFrame(rows, columns=columns)

    df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    center_lat, center_lon = gdf['geometry'].y.mean(), gdf['geometry'].x.mean()

    map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        control_scale = True
    )

    for index, row in gdf.iterrows():
        popup_html = f'<a href="/restaurant/{row["id"]}" target="_blank">{row["restaurant_name"]}</a>'
        print(popup_html)
        folium.Marker(
            location = [row.geometry.y, row.geometry.x],
            popup = folium.Popup(popup_html, max_width=300),
        ).add_to(map)

    map_html = map._repr_html_()
            
    return map_html