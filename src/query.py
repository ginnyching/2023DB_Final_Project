from pyspark.sql import SparkSession
from pyspark.sql.functions import *

import geopandas as gpd
import contextily as cx
import matplotlib.pyplot as plt

month_names = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

spark = SparkSession.builder.appName('DB_Final_Project')\
                            .config("spark.driver.memory", "8g")\
                            .config("spark.executor.memory", "8g")\
                            .getOrCreate()

taxi= spark.read\
      .option("header", "true")\
      .option("inferSchema", "true")\
      .parquet("./data/yellow_tripdata_2022-01.parquet", 
               "./data/yellow_tripdata_2022-02.parquet", 
               "./data/yellow_tripdata_2022-03.parquet", 
               "./data/yellow_tripdata_2022-04.parquet", 
               "./data/yellow_tripdata_2022-05.parquet", 
               "./data/yellow_tripdata_2022-06.parquet", 
               "./data/yellow_tripdata_2022-07.parquet", 
               "./data/yellow_tripdata_2022-08.parquet", 
               "./data/yellow_tripdata_2022-09.parquet", 
               "./data/yellow_tripdata_2022-10.parquet", 
               "./data/yellow_tripdata_2022-11.parquet", 
               "./data/yellow_tripdata_2022-12.parquet")

taxi=taxi.na.drop(how="any")
taxi=taxi.filter(year(col("tpep_pickup_datetime"))=="2022")
taxi=taxi.distinct()

def hour_distribution(date):
    '''
    date = "2022-mm-dd"
    date = "2022-mm"
    '''
    pickup_by_day=taxi.filter(col("tpep_pickup_datetime").startswith(date))
    pbd_hour=pickup_by_day.select(hour(col("tpep_pickup_datetime")).alias("hour")).groupby("hour").count()
    pbd_hour_pd=pbd_hour.sort("hour").toPandas()
    return pbd_hour_pd

def avg_hour_distribution():
    pickup_hour=taxi.select(hour(col("tpep_pickup_datetime")).alias("hour"), month(col("tpep_pickup_datetime")).alias("month"))
    peak_hour=pickup_hour.groupBy("hour").count().sort(col("count").desc())
    peak_hour_pd=peak_hour.sort("hour").toPandas()
    ax=peak_hour_pd.plot.bar(x="hour",y="count",rot=0,legend=False,figsize=(10,6))
    return peak_hour_pd, ax
    
def avg_month_distribution():
    pickup_hour=taxi.select(hour(col("tpep_pickup_datetime")).alias("hour"), month(col("tpep_pickup_datetime")).alias("month"))
    peak_month=pickup_hour.groupBy("month").count().sort(col("count").desc())
    peak_month_pd=peak_month.sort("month").toPandas()
    ax=peak_month_pd.plot.bar(x="month",y="count",rot=0,legend=False,figsize=(10,6))
    return peak_month_pd, ax

def month_hour_distribution():
    pickup_hour=taxi.select(hour(col("tpep_pickup_datetime")).alias("hour"), month(col("tpep_pickup_datetime")).alias("month"), month(col("tpep_pickup_datetime")).alias("month"), date_format("tpep_pickup_datetime", "MMM").alias("Month_Name"))
    peak_hour = pickup_hour.groupBy("hour", "month", "Month_Name").count()
    peak_hour = peak_hour.drop("Month_Name")
    hour = peak_hour.toPandas()
    hour_m = hour.pivot(index='month', columns='hour', values='count')
    hour_m.index = hour_m.index.map(month_names)
    return hour_m

def pickup_map(date):
    '''
    date = "2022-mm-dd
    date = "2022-mm
    '''
    shapefile_path = "./data/taxi_zones.zip" 
    gdf = gpd.read_file(shapefile_path)
    pickup_by_day=taxi.filter(col("tpep_pickup_datetime").startswith(date))
    pbd_location=pickup_by_day.select(col("PULocationID").alias("LocationID")).groupBy("LocationID").count()
    pbd_location_pd=pbd_location.toPandas()
    gdf_location = gdf.merge(pbd_location_pd, on='LocationID', suffixes=('', '_count'),how="left")
    gdf_location['count'] = gdf_location['count'].fillna(0)
    gdf_location=gdf_location.to_crs(epsg=4326)
    return gdf_location

def dropoff_map(date):
    '''
    date = "2022-mm-dd
    date = "2022-mm
    '''
    shapefile_path = "./data/taxi_zones.zip" 
    gdf = gpd.read_file(shapefile_path)
    pickup_by_day=taxi.filter(col("tpep_pickup_datetime").startswith(date))
    pbd_dolocation=pickup_by_day.select(col("DOLocationID").alias("LocationID")).groupBy("LocationID").count()
    pbd_dolocation_pd=pbd_dolocation.toPandas()
    gdf_dolocation = gdf.merge(pbd_dolocation_pd, on='LocationID', suffixes=('', '_count'),how="left")
    gdf_dolocation['count'] = gdf_dolocation['count'].fillna(0)
    print("Most dropoff zone: ",gdf_dolocation['zone'].loc[gdf_dolocation['count'].idxmax()],
        " in ",gdf_dolocation['borough'].loc[gdf_dolocation['count'].idxmax()],
        f" borough, having {gdf_dolocation['count'].max()}  dropoffs.")
    gdf_dolocation=gdf_dolocation.to_crs(epsg=4326)
    return gdf_dolocation
