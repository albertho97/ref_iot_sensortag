#from __future__ import print_function
import time
import json
import boto3

print('Loading function')
      
def main(event, context):
    print(event)
    
    client = boto3.client('iot-data', region_name='ap-northeast-1')

    isTooHotState = "false"
    if event['IRTemp'] > 28:
        isTooHotState = "true"

    wasTooHot = None
    try:
        response = client.get_thing_shadow(thingName='SensorTagGateway')
        streamingBody = response["payload"]
        jsonState = json.loads(streamingBody.read())
        wasTooHot = jsonState.get("state").get("reported").get(event.get('DeviceName')).get('isTooHot')
    
    except Exception, e:
        print e
    
    print wasTooHot
    if wasTooHot == isTooHotState:
        return
    else:
        print ("Switched state") 
    
    state = '{ "state": { "reported": { "' + event['DeviceName'] + '": { "isTooHot": "' + isTooHotState + '" } } } }'
    mypayload = json.dumps(state)
    
    response = client.update_thing_shadow(
        thingName='SensorTagGateway',
        payload=state
    )
    return "Shadow set completed"        

def lambda_handler(event, context):
    main(event, context)
  
  
if __name__ == '__main__':
    main('blank', 'blank')