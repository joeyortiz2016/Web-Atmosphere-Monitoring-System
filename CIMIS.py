import json
import requests
import datetime
import time

def roundTime(input_time):
    minute = input_time.minute

    if (minute >= 30):
        hour = input_time + datetime.timedelta(hours=1)
        time_string = hour.strftime('%H')
        time_string = time_string + '00'
        if(time_string == '0000'):
            time_string = '2400'
        return time_string
    time_string = input_time.strftime('%H') + '00'
    if(time_string == '0000'):
        time_string = '2400'
    return time_string
    

def getCIMIS(input_time):
    date = datetime.datetime.now()
    sDate = date - datetime.timedelta(days=1)
    time_string = roundTime(input_time)
    date_string = str(input_time.date())
    print("date_string =", date_string)
    print("time_string =", time_string)
    URL = "http://et.water.ca.gov/api/data"
    appkey = "843a0cff-be6b-4107-9bb4-2af790f4d094"
    targets = "75"
    EndDate = str(date.year) + '-' + str(date.month)+ '-' + str(date.day)
    StartDate = str(sDate.year) + '-' + str(sDate.month)+ '-' + str(sDate.day)
    unitOfMeasure = "M"
    dataItems = "hly-air-tmp, hly-rel-hum, hly-eto"
        
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        
    PARAMS = {'appKey':appkey,
              'targets':targets,
              'startDate':StartDate,
              'endDate':EndDate,
              'unitOfMeasure':unitOfMeasure,
              'dataItems':dataItems}
    print("Requesting data from CIMIS website...")
    time.sleep(.5)
    try:
        r = requests.get(url = URL, params = PARAMS).json()
    except requests.exceptions.RequestException as e:
        print("Uh oh! CIMIS website is down! Returning none...")
        print("\n\n")
        print(e)
        print("\n\n")
        return None

    if (r == None):
        print("Request error!")
    data = r
    #print(r.status_code)
    with open('data.json', 'w') as f:
        json.dump(data,f)
    #print(data)    
    if (data['Data']['Providers'][0]['Records'][0]['Date'] == None and data['Data']['Providers'][0]['Records'][0]['Hour'] == None and data['Data']['Providers'][0]['Records'][0]['HlyAirTmp']['Value'] == None and data['Data']['Providers'][0]['Records'][0]['HlyRelHum']['Value'] == None and data['Data']['Providers'][0]['Records'][0]['HlyEto']['Value'] == None):
        print("Could not access data...")
        return None

    date = data['Data']['Providers'][0]['Records'][0]['Date']
    hour = data['Data']['Providers'][0]['Records'][0]['Hour']
    temp = data['Data']['Providers'][0]['Records'][0]['HlyAirTmp']['Value']
    hum = data['Data']['Providers'][0]['Records'][0]['HlyRelHum']['Value']
    eto = data['Data']['Providers'][0]['Records'][0]['HlyEto']['Value']


    i = 0
    while (i <= 47):
        date = data['Data']['Providers'][0]['Records'][i]['Date']
        hour = data['Data']['Providers'][0]['Records'][i]['Hour']
        temp = data['Data']['Providers'][0]['Records'][i]['HlyAirTmp']['Value']
        hum = data['Data']['Providers'][0]['Records'][i]['HlyRelHum']['Value']
        eto = data['Data']['Providers'][0]['Records'][i]['HlyEto']['Value']
        #if (i == 22):
        #break
        if(i < 47):
            f_temp = data['Data']['Providers'][0]['Records'][i+1]['HlyAirTmp']['Value']
        if (f_temp == None or (time_string == hour and date_string == date)):
            break
        i += 1

    if (time_string != hour or date_string != date):
        print("Resources for requested time are not updated!")
        print("Requested time: ", time_string)
        print("Time got from CIMIS station: ", hour)
        print(date)
        print("\n")
        return None        

##    date = '2019-13-6'
##    hour = '2300'
##    temp = '29'
##    hum = '67'
##    eto = '0.01'
    List = [date, hour, temp, hum, eto]
    print(date)
    print(hour)
    print(temp, "C")
    print(hum, "%")
    print(eto, "mm")
    print("time_string = ", time_string)
    time.sleep(1)
    return List
##    except requests.exceptions.RequestException as e:
##        print("There was an exception!")
##        List = None
##        return List


##while True:
##    b = datetime.datetime.now() - datetime.timedelta(hours=1)
##    print("\n\n")
##    print("this is the current time: ", b)
##    a = getCIMIS(b)
##    current = datetime.datetime.now() - datetime.timedelta(hours=1)
##    a = roundTime(current)
##    print(a)

