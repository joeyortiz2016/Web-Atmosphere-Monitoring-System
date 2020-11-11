import CIMIS
import datetime
def getETOlocal(temp, hum, current):
    #current = datetime.datetime.now() - datetime.timedelta(hours=1)
    values = CIMIS.getCIMIS(current)
    if(values == None):
        return None
    print(values)
    stationTemp = values[2].split(" ")
    stationHum = values[3].split(" ")
    stationETO = values[4].split(" ")
    localETO = float(stationETO[0]) * (temp/float(stationTemp[0])) *(float(stationHum[0])/hum)
    local_gal = (localETO * 1 * 1500 * .62)/.75
    station_gal = (float(stationETO[0]) * 1 *1500 *.62)/.75
    getVal = [temp, hum, float(localETO), float(stationTemp[0]), float(stationHum[0]), float(stationETO[0]), local_gal, station_gal]
    return getVal


