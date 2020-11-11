import RPi.GPIO as GPIO
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import I2CLCD1602
import CIMIS
import getETOlocal as ETO
import DHT11 as DHT
import threading
import datetime
import time

irrigation=0 #global variable to determine whether to irrigate or not
irrigationTime = 0 #the time it takes to irrigate 
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
        mcp = PCF8574_GPIO(PCF8574_address)
except:
        try:
                mcp = PCF8574_GPIO(PCF8574A_address)
        except:
                print ('I2C Address Error !')
                exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

##################Setting Up PIR SENSOR and addding Interrupt#####################################
sensorPin=7 #define the sensorPin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin,GPIO.IN,GPIO.PUD_DOWN)

def detection(sensorPin):
    print("Motion has been detected!\n")
    global irrigation, lcd
    if(GPIO.input(sensorPin)==GPIO.HIGH and irrigation==1):
        print("Turning off the irrigation\n")
        irrigation=0
        t=threading.Thread(target=motion_thread)
        t.daemon = True
        t.start()
        

def motion_thread():
    print("Starting Motion Thread\n")
    GPIO.remove_event_detect(sensorPin)
    start=time.time()
    global irrigation, lcd
    while(GPIO.input(sensorPin)==GPIO.HIGH and (time.time()-start)<60):
        irrigation=0
    print("Turning Irrigation back on\n")
    lcd.clear()
    lcd.setCursor(0,0)  # set cursor position
    lcd.message( "IRRIGATION ON")
    elapsed=time.time()-start
    print(elapsed)
    irrigation=1
    GPIO.add_event_detect(sensorPin,GPIO.RISING,detection)
    return

GPIO.add_event_detect(sensorPin,GPIO.RISING,detection)

########################################################
###########Setting Up Relay and Motor#########
relayPin = 31    # define the relayPin
buttonPin = 32    # define the buttonPin
debounceTime = 50
GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
GPIO.setup(buttonPin, GPIO.IN)
relayState = False
GPIO.output(relayPin,GPIO.LOW)
def buttonDetect():
        global relayState, debounceTime
        lastChangeTime = round(time.time()*1000)
        buttonState = GPIO.HIGH
        lastButtonState = GPIO.HIGH
        reading = GPIO.HIGH
        while True:
                reading = GPIO.input(buttonPin)         
                if reading != lastButtonState :
                        lastChangeTime = round(time.time()*1000)
                if ((round(time.time()*1000) - lastChangeTime) > debounceTime):
                        if reading != buttonState :
                                buttonState = reading;
                                if buttonState == GPIO.LOW:
                                        print("Button is pressed!")
                                        relayState = not relayState
                                        if relayState:
                                                print("Turn on relay ...")
                                        else :
                                                print("Turn off relay ... ")
                                else :
                                        print("Button is released!")
                lastButtonState = reading
                
buttonThread = threading.Thread(target=buttonDetect)
buttonThread.daemon = True
buttonThread.start()

def runningIrrigation():
        global irrigation, irrigationTime, irrigateStart, relayState
        timeStart = time.time()
        print(time.time())
        elapsedTime = 0
        while True:
                elapsedTime = time.time() - timeStart
                if (irrigation == 1 and elapsedTime < irrigationTime):
                        GPIO.output(relayPin,relayState)
                if(irrigation == 0 and elapsedTime < irrigationTime):
                        timeStart = time.time() - elapsedTime
                        GPIO.output(relayPin,GPIO.LOW)
                if(elapsedTime > irrigationTime):
                        GPIO.output(relayPin,GPIO.LOW)
                        break
        #irrigation = 0
        return
########################################
#if __name__ == '__main__':
 #   print ('Program is starting ... ')
  #  try:
   #     loop()
    #except KeyboardInterrupt:
     #   destroy()
sensorPin = 7

local_temp = None
local_hum = None
local_ETo = None 
cimis_ETo = None 
cimis_temp = None
cimis_hum = None
local_gal = None
station_gal = None
data_temp = None
data_hum = None
data_eto =None
web_temp = None
web_hum = None
web_eto = None
local = [local_temp, local_hum, local_ETo]
CIMIS = [cimis_temp, cimis_hum, cimis_ETo]
LCDdata = [data_temp, data_hum, data_eto,web_temp, web_hum, web_eto, local_gal, station_gal]#last averages to put on the LCD
overallStart = time.time()  #get total time


def get_temp():
        dhtO = DHT.DHTReaderbb()
        print("Starting loop...")
        temp = dhtO.tempAvg
        humidity = dhtO.humidAvg
        value = [temp, humidity]
        if(value[0] != 0): #making sure not passing invalid averages
                LCDdata[0] = value[0]
                LCDdata[1] = value[1]
        return(value)

def displayLCD():
        print("Child thread running...")
        global LCDdata, local, CIMIS, overallStart, mcp, lcd
        while True:
                if irrigation == 0:
                        lcd.clear()
                        lcd.setCursor(0,0)  # set cursor position
                        lcd.message( "IRRIGATION OFF")
                        time.sleep(5)
                if( local[0] != None and CIMIS[0] != None and LCDdata[0] != None and irrigation == 1):
                        lcd.clear()
                        lcd.setCursor(0,0)  # set cursor position
                        lcd.message( "IRRIGATION ON")
                        time.sleep(30)
                        lcd.clear()
                        I2CLCD1602.loop(LCDdata, lcd)
                        

            
        
#keep track of CIMIS time
local_lib = []
CIMIS_time =0


I2CLCD1602.begin(mcp, lcd)
def startLCD():
        while True:
                if( local[0] != None and CIMIS[0] != None and LCDdata[0] != None):
                        thread1 = threading.Thread(target=displayLCD)
                        thread1.daemon= True
                        thread1.start()
                        break
        return

start_thread = threading.Thread(target=startLCD)
start_thread.start()

while True:
    print("Main thread running...")
    size = len(local_lib)
    print(size)
    if (size != 0):
           counter = 0
           local[0] = 0
           local[1] = 0
           local[2] = 0
           CIMIS[0] = 0
           CIMIS[1] = 0
           CIMIS[2] = 0
           local_gal = 0
           station_gal = 0
           while (counter < size):
                    current_lib = local_lib[counter]
                    eto = ETO.getETOlocal(current_lib[0], current_lib[1], current_lib[2])
                    if (eto == None):
                            break
                    local[0] += eto[0]
                    local[1] += eto[1]
                    local[2] += eto[2]
                    CIMIS[0] += eto[3]
                    CIMIS[1] += eto[4]
                    CIMIS[2] += eto[5]
                    local_gal += eto[6]
                    station_gal += eto[7]
                    counter = counter + 1
           i = 0
           while(i<counter):
                local_lib.pop(0)
                i += 1
           if counter > 0:
                   local[0] = local[0]/counter
                   local[1] = local[1]/counter
                   local[2] = local[2]/counter
                   CIMIS[0] = CIMIS[0]/counter
                   CIMIS[1] = CIMIS[1]/counter
                   CIMIS[2] = CIMIS[2]/counter
                   local_gal = local_gal/counter
                   station_gal = station_gal/counter
                   LCDdata[0] = local[0]
                   LCDdata[1] = local[1]
                   LCDdata[2] = local[2]
                   LCDdata[3] = CIMIS[0]
                   LCDdata[4] = CIMIS[1]
                   LCDdata[5] = CIMIS[2]
                   LCDdata[6] = local_gal
                   LCDdata[7] = station_gal
                   if(local_gal > 0):
                           irrigation = 1
           if(irrigation == 1 and eto != None):
                    gallons = eto[6]
                    irrigationTime = (3600/1020) * gallons
                    threadIrrigate = threading.Thread(target=runningIrrigation)
                    threadIrrigate.daemon = True
                    threadIrrigate.start()

    
    getVal = get_temp()
    CIMIS_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    eto = ETO.getETOlocal(getVal[0], getVal[1], CIMIS_time)
    if (eto == None):
            local_values = [getVal[0], getVal[1], CIMIS_time]
            local_lib.append(local_values)
            gallons = 1020
            irrigationTime = (3600/1020) * gallons
            irrigation = 1
            continue
    print("ETo is ", eto)
    if(eto != None):
            local[0] = eto[0]
            local[1] = eto[1]
            local[2] = eto[2]
            CIMIS[0] = eto[3]
            CIMIS[1] = eto[4]
            CIMIS[2] = eto[5]
            LCDdata[0] = local[0]
            LCDdata[1] = local[1]
            LCDdata[2] = local[2]
            LCDdata[3] = CIMIS[0]
            LCDdata[4] = CIMIS[1]
            LCDdata[5] = CIMIS[2]
            LCDdata[6] = eto[6]
            LCDdata[7] = eto[7]
            if(eto[6] > 0):
                    irrigation = 1
    if(irrigation == 1 and eto != None):
        gallons = eto[6]
        irrigationTime = (3600/1020) * gallons
        threadIrrigate = threading.Thread(target=runningIrrigation)
        threadIrrigate.daemon = True
        threadIrrigate.start()

    elapsedtime = time.time() - (overallStart) #track of overall time to get 24 hours
    if (elapsedtime > 86520): #24 hours + 2 minutes
        print("24 hours have passed!")
        break
        #time.sleep(1)
    print("Overall time is ", elapsedtime)


    
    
    
    


