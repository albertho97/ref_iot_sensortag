import boto
import json
import threading
import paho.mqtt.client as mqtt
import sys
import ssl
import RPi.GPIO as GPIO
    
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/RaspberryPiGateway/shadow/update/accepted", qos=1)

    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos) + "data" + str(obj))

def on_message(mqttc, obj, msg):

    jsonState = json.loads(msg.payload)    
    #print jsonState
    
    deviceJson = jsonState.get('state').get('reported')
    
    isTooDark = deviceJson.get(deviceJson.keys()[0]).get('isTooDark')
    isTooHot = deviceJson.get(deviceJson.keys()[0]).get('isTooHot')
    
    if isTooDark:
        if isTooDark == "true":
            GPIO.setup(17,GPIO.OUT)
            GPIO.output(17,GPIO.HIGH)
            print ("Blue Light On")
        elif isTooDark == "false":
            GPIO.setup(17,GPIO.OUT)
            GPIO.output(17,GPIO.LOW)
            print ("Blue Light Off")

    if isTooHot:
        if isTooHot == "true":
            GPIO.setup(27,GPIO.OUT)
            GPIO.output(27,GPIO.HIGH)
            print ("Red Light On")
        elif isTooHot == "false":
            GPIO.setup(27,GPIO.OUT)
            GPIO.output(27,GPIO.LOW)
            print ("Red Light Off")

    
def main():
    print ("Temperature off")
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setup(27,GPIO.OUT)
    GPIO.output(27,GPIO.LOW)
    GPIO.setup(17,GPIO.OUT)
    GPIO.output(17,GPIO.LOW)    

    mqttc = mqtt.Client()
    
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_message = on_message

    mqttc.tls_set("./certs/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem",
            certfile="./certs/cb3727e233-certificate.pem.crt",
            keyfile="./certs/cb3727e233-private.pem.key",
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None )

    mqttc.connect("A17HTFKPRO3T19.iot.ap-northeast-1.amazonaws.com", 8883, 10)    
    print ("Connected sucessfully")
        
    mqttc.loop_forever()

    GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setup(27,GPIO.OUT)
    GPIO.output(27,GPIO.LOW)
    GPIO.setup(17,GPIO.OUT)
    GPIO.output(17,GPIO.LOW)        

if __name__ == '__main__':
    main()
