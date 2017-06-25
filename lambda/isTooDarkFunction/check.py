#from __future__ import print_function
import time
import json
import boto3
import botocore

print('Loading function')
      
def main(event, context):
    print(event)
    
    client = boto3.client('iot-data', region_name='ap-northeast-1')

    isTooDarkState = "false"
    if event['Lux'] <= 15:
        isTooDarkState = "true"
        
    wasTooDark = None
    try:
        response = client.get_thing_shadow(thingName='SensorTagGateway')
        streamingBody = response["payload"]
        jsonState = json.loads(streamingBody.read())
        wasTooDark = jsonState.get("state").get("reported").get(event.get('DeviceName')).get('isTooDark')
    
    except Exception, e:
        print e
        
    print wasTooDark
    if wasTooDark == isTooDarkState:
        return
    else:
        print ("Switched state")
    
    state = '{ "state": { "reported": { "' + event['DeviceName'] + '": { "isTooDark": "' + isTooDarkState + '" } } } }'
    mypayload = json.dumps(state)
    
    response = client.update_thing_shadow(
        thingName='SensorTagGateway',
        payload=state
    )
    return "Shadow set completed"        

def lambda_handler(event, context):
    main(event, context)
  
  
if __name__ == '__main__':
    dummy = {u'Lux': 546.24, u'DeviceName': u'aws1'}
    main(dummy, 'blank')