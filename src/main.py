import contextily as cx
import matplotlib.pyplot as plt
plt.switch_backend('Agg') 

from query import *
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/pythonScript')
def mainJs():
    print("read from js: ")
    select = request.args.get('type')
    dataOne = request.args.get('dataOne')
    dataTwo = request.args.get('dataTwo')
    print(select)
    print(dataOne)
    print(dataTwo)
    if select=="1":
        if dataTwo=="0":
            pbd_hour_pd = hour_distribution("2022-" + dataOne)
            pbd_hour_pd.plot.bar(x='hour', y='count')
            plt.plot(pbd_hour_pd["hour"],pbd_hour_pd["count"],color="r",marker=".")
            plt.title(f"Pickup Hour Distribution of {dataOne}")
            plt.xlabel("hour")
            plt.ylabel("count")
            plt.xticks(rotation=0)
            plt.savefig("./src/static/image/" + dataOne + "_hour.png")
            plt.clf()
        else: 
            pbd_hour_pd = hour_distribution("2022-" + dataOne + "-" + dataTwo)
            pbd_hour_pd.plot.bar(x='hour', y='count')
            plt.plot(pbd_hour_pd["hour"],pbd_hour_pd["count"],color="r",marker=".")
            plt.title(f"Pickup Hour Distribution of {dataOne} / {dataTwo}")
            plt.xlabel("hour")
            plt.ylabel("count")
            plt.xticks(rotation=0)
            plt.savefig("./src/static/image/" + dataOne + "_" + dataTwo + "_hour.png")
            plt.clf()
    if select=="2":
        peak_hour_pd, ax = avg_hour_distribution()
        peak_hour_pd.plot.line("hour",ax=ax,color="red",label=".")
        plt.title("Pickup Hour Distribution",fontsize=25)
        plt.xlabel("hour",fontsize=20)
        plt.ylabel("count",fontsize=20)
        plt.grid(axis='y', linewidth = 0.5)
        plt.savefig("./src/static/image/hour.png")
        plt.clf()
    if select=="3":
        peak_month_pd, ax = avg_month_distribution()
        peak_month_pd.plot.line(ax=ax,color="red",label=".")
        plt.title("Pickup month Distribution",fontsize=25)
        plt.xlabel("month",fontsize=20)
        plt.ylabel("count",fontsize=20)
        plt.grid(axis='y', linewidth = 0.5)
        plt.savefig("./src/static/image/month.png")
        plt.clf()
    if select=="4":
        if dataTwo=="0":
            gdf_location = pickup_map("2022-" + dataOne)
            fig, ax = plt.subplots(figsize=(12, 10))
            gdf_location.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='k', alpha=0.9,legend=True)
            cx.add_basemap(ax,crs=gdf_location.crs)
            ax.set_title(f'Pickup Location Heat Map of {dataOne}')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            plt.savefig("./src/static/image/" + dataOne + "_pickup.png")
            plt.clf()
        else: 
            gdf_location = pickup_map("2022-" + dataOne + "-" + dataTwo)
            fig, ax = plt.subplots(figsize=(12, 10))
            gdf_location.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='k', alpha=0.9,legend=True)
            cx.add_basemap(ax,crs=gdf_location.crs)
            ax.set_title(f'Pickup Location Heat Map of {dataOne} / {dataTwo}')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            plt.savefig("./src/static/image/" + dataOne + "_" + dataTwo + "_pickup.png")
            plt.clf()
    if select=="5":
        if dataTwo=="0":
            gdf_dolocation = dropoff_map("2022-" + dataOne)
            fig, ax = plt.subplots(figsize=(12, 10))
            gdf_dolocation.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='k', alpha=0.9,legend=True)
            cx.add_basemap(ax,crs=gdf_dolocation.crs)
            ax.set_title(f'Dropoff Location Heap Map of {dataOne}')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            plt.savefig("./src/static/image/" + dataOne + "_dropoff.png")
            plt.clf()
        else: 
            gdf_dolocation = dropoff_map("2022-" + dataOne + "-" + dataTwo)
            fig, ax = plt.subplots(figsize=(12, 10))
            gdf_dolocation.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='k', alpha=0.9,legend=True)
            cx.add_basemap(ax,crs=gdf_dolocation.crs)
            ax.set_title(f'Dropoff Location Heap Map of {dataOne} / {dataTwo}')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            plt.savefig("./src/static/image/" + dataOne + "_" + dataTwo + "_dropoff.png")
            plt.clf()
    return jsonify("done")

@app.route('/')
def index():
    return render_template('/index.html')

if __name__ == "__main__":
    app.run(debug=True)
