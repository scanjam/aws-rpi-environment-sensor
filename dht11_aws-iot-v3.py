#Program to read the values of Temp and Hum from the DHT11 sensor and send it over to AWS-IOT

#Website: www.circuitdigest.com

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #Import from AWS-IoT Library
import time#To create delay
from datetime import date, datetime #To get date and time
import adafruit_dht #Import DHT Library for sensor
import board

myMQTTClient = AWSIoTMQTTClient("new_Client")
myMQTTClient.configureEndpoint("a1721k2gh9d1iv-ats.iot.eu-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/code/certs/Amazon-root-CA-1.pem", "/home/pi/code/certs/private.pem.key", "/home/pi/code/certs/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

sensor_name = adafruit_dht.DHT11 #we are using the DHT11 sensor
sensor_pin = 4 #The sensor is connected to GPIO4 on Pi

time.sleep(2) #wait for 2 secs
connecting_time = time.time() + 10

if time.time() < connecting_time:  #try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish("DHT11/info", "connected", 0)
    print("MQTT Client connection success!")
else:
    print("Error: Check your AWS details in the program")
    

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
while True:
    try:
        now = datetime.utcnow() #get date and time 
        current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ') #get current time in string format
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(2.0)

    #prepare the payload in string format 
    payload = '{ "timestamp": "' + current_time + '","temperature": ' + str(temperature_c) + ',"humidity": '+ str(humidity) + ' }'
    print(payload) #print payload for reference 
    myMQTTClient.publish("DHT11/data", payload, 0) #publish the payload
    
    time.sleep(2) #Wait for 2 sec then update the values


