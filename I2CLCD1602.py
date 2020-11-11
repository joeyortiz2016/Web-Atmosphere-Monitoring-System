#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import DHT11 as DHT
import getETOlocal as ETO
import time
from time import sleep, strftime
from datetime import datetime, timedelta
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('LastTime:%H:%M')
	
def get_hour_later():
    an_hour_from_now = datetime.now() + timedelta(hours=1)
    return '{:%H:%M}'.format(an_hour_from_now)

	

def loop(data, lcd):
    sleep(5)
    #lcd.clear()
    lcd.setCursor(0,0)  # set cursor position
    #lcd.message( 'T:' +  '{:.2f}'.format(Local[0])+ "C" + 'H:' + '{:.2f}'.format(Local[1]) + "%\n") # display CPU temperature
    #lcd.message( get_time_now() )   # display the time
    
    scroll_msg = 'Local: ' +'T:' +  '{:.2f}'.format(data[0])+ "C " + 'H:' + '{:.2f}'.format(data[1]) + '% ' + 'Local ETo:' + '{:.2f}'.format(data[2])  + ' Local Gallons Est.:' + '{:.2f}'.format(data[6])+ " \n"
    second_msg = 'CIMIS: ' + 'T:' +  '{:.2f}'.format(data[3])+ "C " + 'H:' + '{:.2f}'.format(data[4]) + '% ' + 'CIMIS ETo:' + '{:.2f}'.format(data[5]) + ' CIMIS Gallons Est.:' + '{:.2f}'.format(data[6]) 
    #lcd.message(scroll_msg)
    #lcd.message(second_msg)
    len_scroll = len(scroll_msg) if scroll_msg >= second_msg else len(second_msg)
    # Scroll to the left
    first = 0
    lasti = 30
    last = 31
    while(last < len_scroll):
        for i in range(len_scroll):
            sleep(.05)
            scroll_msgi = scroll_msg[first:lasti] + '\n'
            lcd.message(scroll_msgi)
            lcd.message(second_msg[first:last])
            first += 1
            last += 1
            lasti += 1
    first = 0
    last = 31
    lasti = 30
##            lcd.autoscroll()
##            lcd.DisplayLeft()

def begin(mcp, lcd):  
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    lcd.setCursor(0,0)
    
    # Demo scrolling message LEFT
    lcd.clear()
    scroll_msg = 'Loading... First\n'
    second_msg = 'Value at ' + get_hour_later()
    lcd.message(scroll_msg)
    lcd.message(second_msg)
    len_scroll = len(scroll_msg) if scroll_msg >= second_msg else len(second_msg)
    # Scroll to the left
    #for i in range(16):
    #sleep(0.5)
    #lcd.autoscroll()
    #lcd.DisplayLeft()

def destroy():
    lcd.clear()
    

