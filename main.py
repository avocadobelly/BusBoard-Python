import requests
from api_keys import app_id
from api_keys import app_key

#postcode = input('Input your current postcode:\n')
postcode = "BA12AF"

#CLASSES
class BusStop:

    def __init__(self, code, name):
        self.code = code
        self.name = name
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

        next_buses = []
        for bus in all_bus_departures:
           next_buses.append([bus['line'], bus['aimed_departure_time']])
        return next_buses


# Convert postcode to long and lat
def PostCodetoLatLong(postcode):
    postcode_info = requests.get('https://api.postcodes.io/postcodes/' + postcode)
    json_postcode_info = postcode_info.json()

    longitude = json_postcode_info['result']['longitude']
    latitude = json_postcode_info['result']['latitude']

    return longitude, latitude

# Find two nearest busstops
def FindNearestBusStops(long, lat):
    r = requests.get('https://transportapi.com/v3/uk/places.json?lat=' + str(lat) + '&lon=' + str(
        long) + '&type=bus_stop', params={'app_id': app_id,
                                          'app_key': app_key})
    busStopsInfo = r.json()

    return busStopsInfo


def getBusStopCodeAndName(busStopsInfo):
    codes = []
    names = []
    for i in range(0,len(busStopsInfo['member'])):
        codes.append(busStopsInfo['member'][i]['atcocode'])
        names.append(busStopsInfo['member'][i]['name'])
        i += 1
        return codes, names

# code_2 = nearest_busstops['member'][1]['atcocode']
# Create 2 busstop classes
# BusStop_1 = BusStop(code_1)
# BusStop_2 = BusStop(code_2)



# Print useful data

# for bus in BusStop_1.buses:
#     print('Bus number:' + bus[0] + '    Expected Arrival: ' + bus[1])
# print('\n')
#
# for bus in BusStop_2.buses:
#     print('Bus number:' + bus[0] + '    Expected Arrival: ' + bus[1])
