import struct
import math
import boto
import json
import time
import datetime
import ssl
import paho.mqtt.client as mqtt
import threading
from sensortag import SensorTag
from sensortag import KeypressDelegate

class record:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def getDeviceName(deviceID):
    name = "unknown"
    if deviceID == "68:C9:0B:06:44:09":
        name = "aws1"
    elif deviceID == "C4:BE:84:70:D1:00":
        name = "aws2"
    elif deviceID == "C4:BE:84:71:32:0A":
        name = "aws3"
    elif deviceID == "C4:BE:84:70:91:0E":
        name = "aws4"
    elif deviceID == "C4:BE:84:71:6E:04":
        name = "aws4"
    else:
        name = "unknown"       
    return name    
    
def publish_readings():

    data = record()
    data.DeviceID = host
    data.DeviceName = getDeviceName(host)
        
    values = tag.IRtemperature.read()
    data.IRTemp, data.AmbientTemp = values[1], values[0]

    values = tag.humidity.read()
    data.Humidity = values[1]

    #values = tag.barometer.read()
    #print tag.barometer.read()
    #data.Barometer = values[1]

    #values = tag.accelerometer.read()
    #print tag.accelerometer.read()
    #data.MagX, data.MagY, data.MagZ = values[0], values[1], values[2]            

    values = tag.magnetometer.read()
    data.MagX, data.MagY, data.MagZ = values[0], values[1], values[2]               
    
    values = tag.gyroscope.read()
    data.GyroX, data.GyroY, data.GyroZ = values[0], values[1], values[2]             

    values = tag.lightmeter.read()
    data.Lux = values
    
    data.WhenCreated = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    pattern = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(data.WhenCreated, pattern)))
    data.time = epoch

    print (data.to_JSON())  
    client.publish("SensorTag/sensors", data.to_JSON())
    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    do_every(1, publish_readings)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
            
def main():
    import time
    import sys
    import argparse
    
    global client
    global host
    global tag

    parser = argparse.ArgumentParser()
    parser.add_argument('-host', action='store',help='MAC of BT device', default='68:C9:0B:06:44:09')
    
    arg = parser.parse_args(sys.argv[1:])

    while True:   
        tag = None
        client = None     
        try:      
    
            host = arg.host
            print('Connecting to ' + host)    
            tag = SensorTag(arg.host)
            
            # Enabling selected sensors
            tag.IRtemperature.enable()
            tag.humidity.enable()
            tag.barometer.enable()
            tag.accelerometer.enable()
            tag.magnetometer.enable()
            tag.gyroscope.enable()
            tag.keypress.enable()
            tag.setDelegate(KeypressDelegate())
            tag.lightmeter.enable()

            # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
            # Not waiting here after enabling a sensor, the first read value might be empty or incorrect.
            time.sleep(1.0)

            print('Connecting to IOT ' + host)
                        
            counter=1
            while True:  
            
                client = mqtt.Client()            
                #client.on_connect = on_connect
                #client.on_message = on_message

                client.tls_set( "/home/pi/certs/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem",
                        certfile="/home/pi/certs/67463260e3-certificate.pem.crt",
                        keyfile="/home/pi/certs/67463260e3-private.pem.key",
                        tls_version=ssl.PROTOCOL_TLSv1_2,
                        ciphers=None )

                client.connect("ae1ocwjl5a0ho.iot.ap-northeast-1.amazonaws.com", 8883, 10)
                publish_readings()
                client.disconnect()   
                #client.loop_forever()

                tag.waitForNotifications(0.5)                

        except:
            print "Unexpected error:", sys.exc_info()[0]
            if tag is not None:
                tag.disconnect()

            del tag
            time.sleep(4.0)

    tag.disconnect()
    del tag
    

if __name__ == "__main__":
    main()
