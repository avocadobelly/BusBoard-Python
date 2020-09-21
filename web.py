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
    busStops = FindNearestBusStops(long, lat)
    code = busStops['member'][0]['atcocode']
    busStop = BusStop(code)
    return render_template('info.html', postcode=postcode, busStop=busStop)

if __name__ == "__main__": app.run()