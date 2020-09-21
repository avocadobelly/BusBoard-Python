from flask import Flask, render_template, request
from main import BusStop, FindNearestBusStops, PostCodetoLatLong, getBusStopCodeAndName

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    long, lat = PostCodetoLatLong(postcode)
    busStopsInfo = FindNearestBusStops(long, lat)
    codes, names = getBusStopCodeAndName(busStopsInfo)
    busStops = []
    busStops.append(BusStop(codes[0], names[0]))

    return render_template('info.html', postcode=postcode, busStops=busStops)

if __name__ == "__main__": app.run()