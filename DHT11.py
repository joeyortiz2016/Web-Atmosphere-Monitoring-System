#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
import logging

DHTPin = 11              #define the pin of DHT11
sleepTime = 60            #time between getting the next reading
howMany2Avg = 60    #how many values before generating averages
logging.basicConfig(filename='test_log', level=logging.DEBUG)
humidAvg = 0
tempAvg = 0

class DHTReaderbb(object):
	def __init__(self):
		logging.debug('DHT Program is starting ... ')
		start_time = time.time()
		time.sleep(5) #giving the program time to get ready
		dht = DHT.DHT(DHTPin)   #create a DHT class object
		sumCnt = 0              #number of reading times
		validCnt = 0            #number of times a valid reading gets through
		tempSum = 0             #sum of all temp
		humidSum = 0            #sum of all humidity
		while(True):
			sumCnt += 1         #counting number of reading times
			chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
			print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
			if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
				print("DHT11,OK!")
				validCnt += 1
				tempSum += dht.temperature
				humidSum += dht.humidity
			elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
				print("DHTLIB_ERROR_CHECKSUM!!")
			elif(chk is dht.DHTLIB_ERROR_TIMEOUT):  #reading DHT times out
				print("DHTLIB_ERROR_TIMEOUT!")
			else:               #other errors
				print("Other error!")

			elapsed_time = time.time() - start_time #get the elapsed time
			print("Humidity : %.2f, \t Temperature : %.2f \n Elapsed time: %.2f \n"%(dht.humidity,dht.temperature,elapsed_time))

		#print out the averages and clear the variables once reached the hM2A variable
			if (sumCnt >= howMany2Avg): #use sumCnt because we're average every hour not by how many
				if(validCnt == 0): #case where all values failed
					print("ERROR")
					self.humidAvg = self.tempAvg = 0
				else:
					self.humidAvg = humidSum / validCnt
					self.tempAvg = tempSum / validCnt
					print("Grabbed %d values to get AVERAGE for Humidity : %.2f, \t Temperature : %.2f \n"%(validCnt, self.humidAvg, self.tempAvg))
					tempSum = humidSum = validCnt = sumCnt = 0 #reset the values
					break

			time.sleep(sleepTime) #wait for 'sleepTime' seconds before grabbing the next value

	#if __name__ == '__main__':
		# try:
			# loop()
		# except KeyboardInterrupt:
			# GPIO.cleanup()
			# exit()

