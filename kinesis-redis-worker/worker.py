# Copyright 2013-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from __future__ import print_function

import sys
import re
import boto
import argparse
import json
import threading
import time
import datetime
import redis

from argparse import RawTextHelpFormatter
from boto.kinesis.exceptions import ProvisionedThroughputExceededException
import poster

# To preclude inclusion of aws keys into this code, you may temporarily add
# your AWS credentials to the file:
#     ~/.boto
# as follows:
#     [Credentials]
#     aws_access_key_id = <your access key>
#     aws_secret_access_key = <your secret key>


kinesis = boto.kinesis.connect_to_region("ap-northeast-1")
iter_type_at = 'AT_SEQUENCE_NUMBER'
iter_type_after = 'AFTER_SEQUENCE_NUMBER'
iter_type_trim = 'TRIM_HORIZON'
iter_type_latest = 'LATEST'
r = redis.StrictRedis(host='sensortagredis.g6jsto.0001.apne1.cache.amazonaws.com', port=6379, db=0)

class datarecord:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
     
def process_to_redis(records):
    for record in records:
        jsonstring = record['Data'].lower()
        json_data = json.loads(jsonstring)

        newdata = {"time":json_data["time"], "devicename":json_data["devicename"], "irtemp":json_data["irtemp"], "lux": json_data["lux"]}
        newdatastring = json.dumps(newdata)

        print (newdatastring)                
        r.publish('pubsubCounters', newdatastring)
        
        
        if json_data["lux"] < 5:
            kinesis.put_record(
                stream_name="LightAlert",
                data=newdatastring, partition_key=json_data["deviceid"])
            print ('Lights up')

        if json_data["irtemp"] > 29:
            kinesis.put_record(
                stream_name="TemperatureAlert",
                data=newdatastring, partition_key=json_data["deviceid"])
            print ('Overheat')


class KinesisWorker(threading.Thread):
    """The Worker thread that repeatedly gets records from a given Kinesis
    stream."""
    def __init__(self, stream_name, shard_id, iterator_type, sleep_interval=0.5,
                 name=None, group=None, args=(), kwargs={}):
        super(KinesisWorker, self).__init__(name=name, group=group,
                                          args=args, kwargs=kwargs)
        self.stream_name = stream_name
        self.shard_id = str(shard_id)
        self.iterator_type = iterator_type
        self.sleep_interval = sleep_interval
        self.total_records = 0

    def run(self):
        my_name = threading.current_thread().name
        print ('+ KinesisWorker:', my_name)
        print ('+-> working with iterator:', self.iterator_type)
        response = kinesis.get_shard_iterator(self.stream_name,
            self.shard_id, self.iterator_type)
        next_iterator = response['ShardIterator']
        print ('+-> getting next records using iterator:', next_iterator)

        while True:
            try:
                response = kinesis.get_records(next_iterator, limit=25)
                self.total_records += len(response['Records'])

                if len(response['Records']) > 0:
                    print ('\n+-> {1} Got {0} Worker Records'.format(len(response['Records']), my_name))
                    process_to_redis(response['Records'])
                else:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                next_iterator = response['NextShardIterator']
                time.sleep(self.sleep_interval)
            except ProvisionedThroughputExceededException as ptee:
                print (ptee.message)
                time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Create or connect to a Kinesis stream and create workers
that hunt for the word "egg" in records from each shard.''',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('stream_name',
        help='''the name of the Kinesis stream to either create or connect''')
    parser.add_argument('--sleep_interval', type=float, default=0.5,
        help='''the worker's work loop sleep interval in seconds [default: 0.1]''')

    args = parser.parse_args()

    stream = kinesis.describe_stream(args.stream_name)
    print (json.dumps(stream, sort_keys=True, indent=2, separators=(',', ': ')))
    shards = stream['StreamDescription']['Shards']
    print ('# Shard Count:', len(shards))

    threads = []
    start_time = datetime.datetime.now()
    for shard_id in xrange(len(shards)):
        worker_name = 'shard_worker:%s' % shard_id
        print ('#-> shardId:', shards[shard_id]['ShardId'])
        worker = KinesisWorker(
            stream_name=args.stream_name,
            shard_id=shards[shard_id]['ShardId'],
            # iterator_type=iter_type_trim,  # uses TRIM_HORIZON
            iterator_type=iter_type_latest,  # uses LATEST
            sleep_interval=args.sleep_interval,
            name=worker_name
            )
        worker.daemon = True
        threads.append(worker)
        print ('#-> starting: ', worker_name)
        worker.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    finish_time = datetime.datetime.now()
    duration = (finish_time - start_time).total_seconds()
    total_records = poster.sum_posts(threads)
    print ("-=> Exiting Worker Main <=-")
    print ("  Total Records:", total_records)
    print ("     Total Time:", duration)
    print ("  Records / sec:", total_records / duration)
    print ("  Worker sleep interval:", args.sleep_interval)
