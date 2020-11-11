import RPi.GPIO as GPIO
import time
import threading
sensorPin=7 #define the sensorPin
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorPin,GPIO.IN,GPIO.PUD_DOWN)
   

def detection(sensorPin):
    print("Motion has been detected!\n")
    global irrigation
    activation=GPIO.input(sensorPin)
    if(activation==GPIO.HIGH and irrigation==1):
        print("Turning off the irrigation\n")
        t=threading.Thread(target=motion_thread)
        t.start()
        

def motion_thread():
    print("Starting Motion Thread\n")
    start=time.time()
    global irrigation
    while(GPIO.input(sensorPin)==GPIO.HIGH and (time.time()-start)<60):
        irrigation=0
    print("Turning Irrigation back on\n")
    elapsed=time.time()-start
    print(elapsed)
    irrigation=1

def loop():
    while True:
        #print(GPIO.input(sensorPin))
        x=GPIO.input(sensorPin)
            

def destroy():
    GPIO.cleanup()


    
        

if __name__=='__main__':
    setup()
    GPIO.add_event_detect(sensorPin,GPIO.RISING,detection)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
