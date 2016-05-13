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
package samples;

import java.io.Serializable;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * 
 * This is the data model for the objects being sent through the Amazon Kinesis streams in the samples
 * 
 */
public class KinesisMessageModel implements Serializable {

    public String AmbientTemp;
    public String DeviceID;
    public String DeviceName;
    public String GyroX;
    public String GyroY;
    public String GyroZ;
    public String Humidity;
    public String IRTemp;
    public String Lux;
    public String MagX;
    public String MagY;
    public String MagZ;
    public String WhenCreated;
    public String time;
    
    /**
     * Default constructor for Jackson JSON mapper - uses bean pattern.
     */
    public KinesisMessageModel() {

    }

    public KinesisMessageModel(
         String AmbientTemp,
         String DeviceID,
         String DeviceName,
         String GyroX,
         String GyroY,
         String GyroZ,
         String Humidity,
         String IRTemp,
         String Lux,
         String MagX,
         String MagY,
         String MagZ,
         String WhenCreated,
         String time) {
        this.AmbientTemp = AmbientTemp;
        this.DeviceID = DeviceID;
        this.DeviceName = DeviceName;
        this.GyroX = GyroX;
        this.GyroY = GyroY;
        this.GyroZ = GyroZ;
        this.Humidity = Humidity;
        this.IRTemp = IRTemp;
        this.Lux = Lux;
        this.MagX = MagX;
        this.MagY = MagY;
        this.MagZ = MagZ;
        this.WhenCreated = WhenCreated;
        this.time = time;
    }

    @Override
    public String toString() {
        try {
            return new ObjectMapper().writeValueAsString(this);
        } catch (JsonProcessingException e) {
            return super.toString();
        }
    }

    public String getAmbientTemp() {
        return AmbientTemp;
    }

    public void setAmbientTemp(String AmbientTemp) {
        this.AmbientTemp = AmbientTemp;
    }

    public String getDeviceID() {
        return DeviceID;
    }

    public void setDeviceID(String DeviceID) {
        this.DeviceID = DeviceID;
    }

    public String getDeviceName() {
        return DeviceName;
    }

    public void setDeviceName(String DeviceName) {
        this.DeviceName = DeviceName;
    }

    public String getGyroX() {
        return GyroX;
    }

    public void setGyroX(String GyroX) {
        this.GyroX = GyroX;
    }

    public String getGyroY() {
        return GyroY;
    }
    
    public void setGyroY(String GyroY) {
        this.GyroY = GyroY;
    }

    public String getGyroZ() {
        return GyroZ;
    }

    public void setGyroZ(String GyroZ) {
        this.GyroZ = GyroZ;
    }

    public String getHumidity() {
        return Humidity;
    }

    public void setHumidity(String Humidity) {
        this.Humidity = Humidity;
    }

    public String getIRTemp() {
        return IRTemp;
    }

    public void setIRTemp(String IRTemp) {
        this.IRTemp = IRTemp;
    }
    
    public String getLux() {
        return Lux;
    }

    public void setLux(String Lux) {
        this.Lux = Lux;
    }

    public String getMagX() {
        return MagX;
    }

    public void setMagX(String MagX) {
        this.MagX = MagX;
    }

    public String getMagY() {
        return MagY;
    }

    public void setMagY(String MagY) {
        this.MagY = MagY;
    }

    public String getMagZ() {
        return MagZ;
    }

    public void setMagZ(String MagZ) {
        this.MagZ = MagZ;
    }

    public String getWhenCreated() {
        return WhenCreated;
    }

    public void setWhenCreated(String WhenCreated) {
        this.WhenCreated = WhenCreated;
    }

    public String gettime() {
        return time;
    }

    public void settime(String time) {
        this.time = time;
    }


    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((AmbientTemp == null) ? 0 : AmbientTemp.hashCode());
        result = prime * result + ((DeviceID == null) ? 0 : DeviceID.hashCode());
        result = prime * result + ((DeviceName == null) ? 0 : DeviceName.hashCode());
        result = prime * result + ((GyroX == null) ? 0 : GyroX.hashCode());
        result = prime * result + ((GyroY == null) ? 0 : GyroY.hashCode());
        result = prime * result + ((GyroZ == null) ? 0 : GyroZ.hashCode());
        result = prime * result + ((Humidity == null) ? 0 : Humidity.hashCode());
        result = prime * result + ((IRTemp == null) ? 0 : IRTemp.hashCode());
        result = prime * result + ((Lux == null) ? 0 : Lux.hashCode());
        result = prime * result + ((MagX == null) ? 0 : MagX.hashCode());
        result = prime * result + ((MagY == null) ? 0 : MagY.hashCode());
        result = prime * result + ((MagZ == null) ? 0 : MagZ.hashCode());
        result = prime * result + ((WhenCreated == null) ? 0 : WhenCreated.hashCode());
        result = prime * result + ((MagZ == null) ? 0 : MagZ.hashCode());
        result = prime * result + ((time == null) ? 0 : time.hashCode());
        
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (!(obj instanceof KinesisMessageModel)) {
            return false;
        }
        KinesisMessageModel other = (KinesisMessageModel) obj;
        if (AmbientTemp == null) {
            if (other.AmbientTemp != null) {
                return false;
            }
        } else if (!AmbientTemp.equals(other.AmbientTemp)) {
            return false;
        }
        if (DeviceID == null) {
            if (other.DeviceID != null) {
                return false;
            }
        } else if (!DeviceID.equals(other.DeviceID)) {
            return false;
        }
        if (DeviceName == null) {
            if (other.DeviceName != null) {
                return false;
            }
        } else if (!DeviceName.equals(other.DeviceName)) {
            return false;
        }
        if (GyroX == null) {
            if (other.GyroX != null) {
                return false;
            }
        } else if (!GyroX.equals(other.GyroX)) {
            return false;
        }
        if (GyroY == null) {
            if (other.GyroY != null) {
                return false;
            }
        } else if (!GyroY.equals(other.GyroY)) {
            return false;
        }
        if (GyroZ == null) {
            if (other.GyroZ != null) {
                return false;
            }
        } else if (!GyroZ.equals(other.GyroZ)) {
            return false;
        }
        if (Humidity == null) {
            if (other.Humidity != null) {
                return false;
            }
        } else if (!Humidity.equals(other.Humidity)) {
            return false;
        }
        if (IRTemp == null) {
            if (other.IRTemp != null) {
                return false;
            }
        } else if (!IRTemp.equals(other.IRTemp)) {
            return false;
        }
        if (Lux == null) {
            if (other.Lux != null) {
                return false;
            }
        } else if (!Lux.equals(other.Lux)) {
            return false;
        }
        if (MagX == null) {
            if (other.MagX != null) {
                return false;
            }
        } else if (!MagX.equals(other.MagX)) {
            return false;
        }
        if (MagY == null) {
            if (other.MagY != null) {
                return false;
            }
        } else if (!MagY.equals(other.MagY)) {
            return false;
        }
        if (MagZ == null) {
            if (other.MagZ != null) {
                return false;
            }
        } else if (!MagZ.equals(other.MagZ)) {
            return false;
        }
        if (WhenCreated == null) {
            if (other.WhenCreated != null) {
                return false;
            }
        } else if (!WhenCreated.equals(other.WhenCreated)) {
            return false;
        }
        if (time == null) {
            if (other.time != null) {
                return false;
            }
        } else if (!time.equals(other.time)) {
            return false;
        }
        
        return true;
    }
}
