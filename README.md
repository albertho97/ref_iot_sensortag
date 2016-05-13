# IOT, SensorTag 2650 and Raspberry Pi - Demo 
This repository demo the integration of AWS IOT, TI SensorTag 2650 and Raspberry Pi 2 (Gateway).


## Pre-requisite

1. https://github.com/IanHarvey/bluepy (GPL 2.0 License)  
The underlying implementation of bluebooth gateway on Raspberry Pi is from Ian Harvey

## Referenced Libraries and Frameworks

1. https://github.com/awslabs/amazon-kinesis-connectors (Amazon Software License)    
Kinesis connectors library are from awslabs, these connectors are used to push data to S3 and redshift.

2. http://epochjs.github.io/epoch/ (MIT License)  
Real Time charting .js library

## High Level Overview

![Alt text](raw/High_Level_Overview.jpg?raw=true "High Level Overview")

Detailed Presentation deck   
[https://github.com/albertho97/aws_iot_sensortag/High_Level_Overview.pdf](High_Level_Overview.pdf)

## Hardware used

![Hardware used](raw/HardwareUsed.jpg?raw=true "Hardware used") ![TI Sensortag 2650](raw/SensorTagVisual.jpg?raw=true "TI Sensortag 2650")

1 x Raspberry Pi 2  
1 x Raspberry Pi B+  
4 x TI CC2650 SensorTag

## Web Application Visualization

![Visualization](raw/Visualization_2.jpg?raw=true "Visualization")

Showing the light sensor readings (Lux) in real-time, there are 4 sensor tag connected to Pi (Gateway) sending data to internet

## AWS Services

Required to be set up behind the scene
- Kinesis
- ElasticCache
- EC2 servers
- Redshift
- S3 bucket
- IAM Policy

## Source code structure 

![Source Code](raw/SourceCode.png?raw=true "Source Code")

Python / NodeJS source required to be installed on devices and EC2 servers. You can refer to above picture, I used “Visual Studio Code” myself to maintain the folder structure, but you can pretty much use any other editor tool.  

### 1.	raspberry-readings-worker
This is the core of everything, this runs on Raspberry Pi 2 Model B, Raspbian OS, gathering readings from the 4 sensortags through “Bluetooth Low Energy”, then fire the data in JSON format to kinesis stream. You need to install Python 2.7, bluez (linux Bluetooth kernel package) and bluepy (python BLE code), have “hciconfig hci0 up” already run, edit the sensortag.py, put in the correct MAC addresses for each SensorTag, then bash start the “push_kinesis_all.sh”.   
This will then sending data to a kinesis stream called “RaspberryPiStream” with 2 shards (which you need to set up beforehand). Once you done all that, you verify everything is coming through the stream first, before moving to the next step. Note : No credentials is hardcoded, so you need to install the AWS Python SDK (boto), get the credentials setup, etc.   

Original Code Reference : ( I have modified the code to make it work with CC2650 )   
https://github.com/IanHarvey/bluepy

### 2.	kinesis-redis-worker
This is a Python kinesis worker running on a c4.large EC2, which consume the data in parallel, based on how many shards there are, then spawn up separate threads to get the kinesis record (JSON data), The workers are doing detection on the “Lux” and “Temperature” readings, once the lux is below 10 (very dark), then it will generate another record into another Kinesis stream “LightAlert”, the same goes for temperature. After that all data are then pass through to “Elastic Cache”.  (which you need to pre-setup yourself)   

Original Code Reference :   
https://github.com/awslabs/kinesis-poster-worker

### 3. sensortag-visual
This is utilized “Epoch” javascript charting library which is based on D3.js, NodeJS, running on a c4.large EC2. This is continuously listening for the redis cache “pub/sub” event. When a client browser first visit the page, the nodeJS start a long polling (persistent connection) to pull for data. Once data arrived, Epoch real-time chart does it job, and dynamically updating the chart. To kick start this daemon, bash start “sensortag-visual.sh”, then use a browser browsing to index.html:9000 for “Temperature Senor” page, index2.html:9000 for “Light Sensor” page.  
Note : You would need to install several NodeJS package, like “redis”, “server-static”, etc   

Original Code Reference :   
http://epochjs.github.io/epoch/  ( for charting )   
https://github.com/awslabs/aws-big-data-blog/tree/master/aws-blog-kinesis-storm-clickstream-app (Original idea from this, but I modify not to use the “Apache Storm” part to simplify the setup. )  

### 4. raspberry-alert-worker  ( Optional )
This runs on Raspberry Pi 2 Model B, Raspbian OS as well, it enrich the demo by having a trigger interaction. When “kinesis-redis-worker” is firing the alerts to “TemperatureAlert” and “LightAlert” kinesis streams, the python client is running locally to retrieve this records, then trigger the LED to lights up.  

You would need to get this ModMyPi kit set up with your Raspberry Pi first though.  
http://www.modmypi.com/raspberry-pi/set-up-kits/project-kits/raspberry-pi-youtube-workshop-kit  

At least you have need to get “Tutorial 2” done, get the LED lights going.  
https://www.youtube.com/watch?v=IP-szuon2Bk  

To kick start the daemon, bash start “long-trigger-temperature.sh”.  

<br />
<br />
# License

Copyright 2016, Amazon Web Services.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and limitations under the License.


