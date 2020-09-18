import requests
from api_keys import app_id
from api_keys import app_key

postcode = 'BA12BL'

#CLASSES
class BusStop:

    def __init__(self, code):
        self.code = code
        self.buses = self.GetBuses()

    def GetBuses(self):
        r = requests.get('https://transportapi.com/v3/uk/bus/stop/' + self.code + '/live.json',
                         params={'app_id': app_id,
                                 'app_key': app_key})
        json_r = r.json()

        all_bus_departures = []
        for single_bus_departures in json_r['departures'].values():
            all_bus_departures = all_bus_departures + single_bus_departures

        all_bus_departures.sort(key=lambda bus: bus["aimed_departure_time"])

        return all_bus_departures


# Convert postcode to long and lat
postcode_info = requests.get('https://api.postcodes.io/postcodes/' + postcode)
json_postcode_info = postcode_info.json()

longitude = json_postcode_info['result']['longitude']
latitude = json_postcode_info['result']['latitude']

# Find two nearest busstops
def FindNearestBusStops(long, lat):
    r = requests.get('https://transportapi.com/v3/uk/places.json?lat=' + str(lat) + '&lon=' + str(
        long) + '&type=bus_stop', params={'app_id': app_id,
                                          'app_key': app_key})
    json_r = r.json()

    return json_r

nearest_busstops = FindNearestBusStops(longitude, latitude)

code_1 = nearest_busstops['member'][0]['atcocode']
code_2 = nearest_busstops['member'][1]['atcocode']

# Create 2 busstop classes
BusStop_1 = BusStop(code_1)
BusStop_2 = BusStop(code_2)

# Print useful data
print(BusStop_1.buses)
