from flask import Flask, render_template, request
from main import BusStop, FindNearestBusStops, PostCodetoLatLong

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    long, lat = PostCodetoLatLong(postcode)
    busStopsInfo = FindNearestBusStops(long, lat)
    code = busStopsInfo['member'][0]['atcocode']
    name = busStopsInfo['member'][0]['name']
    busStops = []
    busStops.append(BusStop(code, name))

    return render_template('info.html', postcode=postcode, busStops=busStops)

if __name__ == "__main__": app.run()