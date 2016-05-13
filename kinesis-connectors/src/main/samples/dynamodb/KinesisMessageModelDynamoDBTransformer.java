/*
 * Copyright 2013-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Amazon Software License (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 * http://aws.amazon.com/asl/
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
package samples.dynamodb;

import java.util.HashMap;
import java.util.Map;

import samples.KinesisMessageModel;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.kinesis.connectors.BasicJsonTransformer;
import com.amazonaws.services.kinesis.connectors.dynamodb.DynamoDBTransformer;

/**
 * A custom transfomer for {@link KinesisMessageModel} records in JSON format. The output is in a format
 * usable for insertions to Amazon DynamoDB.
 */
public class KinesisMessageModelDynamoDBTransformer extends
        BasicJsonTransformer<KinesisMessageModel, Map<String, AttributeValue>> implements
        DynamoDBTransformer<KinesisMessageModel> {

    /**
     * Creates a new KinesisMessageModelDynamoDBTransformer.
     */
    public KinesisMessageModelDynamoDBTransformer() {
        super(KinesisMessageModel.class);
    }

    @Override
    public Map<String, AttributeValue> fromClass(KinesisMessageModel message) {
        Map<String, AttributeValue> item = new HashMap<String, AttributeValue>();
        putStringIfNonempty(item, "AmbientTemp", message.AmbientTemp);
        putStringIfNonempty(item, "DeviceID", message.DeviceID);
        putStringIfNonempty(item, "DeviceName", message.DeviceName);
        putStringIfNonempty(item, "GyroX", message.GyroX);
        putStringIfNonempty(item, "GyroY", message.GyroY);
        putStringIfNonempty(item, "GyroZ", message.GyroZ);
        putStringIfNonempty(item, "Humidity", message.Humidity);
        putStringIfNonempty(item, "IRTemp", message.IRTemp);
        putStringIfNonempty(item, "Lux", message.Lux);
        putStringIfNonempty(item, "MagX", message.MagX);
        putStringIfNonempty(item, "MagY", message.MagY);
        putStringIfNonempty(item, "MagZ", message.MagZ);
        putStringIfNonempty(item, "WhenCreated", message.WhenCreated);
        putStringIfNonempty(item, "time", message.time);
        
        return item;
    }

    /**
     * Helper method to map nonempty String attributes to an AttributeValue.
     * 
     * @param item The map of attribute names to AttributeValues to store the attribute in
     * @param key The key to store in the map
     * @param value The value to check before inserting into the item map
     */
    private void putStringIfNonempty(Map<String, AttributeValue> item, String key, String value) {
        if (value != null && !value.isEmpty()) {
            item.put(key, new AttributeValue().withS(value));
        }
    }

    /**
     * Helper method to map boolean attributes to an AttributeValue.
     * 
     * @param item The map of attribute names to AttributeValues to store the attribute in
     * @param key The key to store in the map
     * @param value The value to insert into the item map
     */
    private void putBoolIfNonempty(Map<String, AttributeValue> item, String key, Boolean value) {
        putStringIfNonempty(item, key, Boolean.toString(value));
    }

    /**
     * Helper method to map nonempty Integer attributes to an AttributeValue.
     * 
     * @param item The map of attribute names to AttributeValues to store the attribute in
     * @param key The key to store in the map
     * @param value The value to insert into the item map
     */
    private void putIntegerIfNonempty(Map<String, AttributeValue> item, String key, Integer value) {
        putStringIfNonempty(item, key, Integer.toString(value));
    }
}
