# azure-iot-temp-humidity
[This python script](temp_humidity_logger.py) logs temperature and humidity data from a [DHT11](https://www.adafruit.com/product/386) temperature and humidity sensor via a [RaspberryPi](https://www.raspberrypi.org/). it then pushes that information up to an endpoint. I am personally using Microsoft Azure Logic Apps for this functionality.




# Prerequisites
## Hardware
The following is a list of the exact hardware I've tested this on:

1. [RaspberryPi Zero](https://www.adafruit.com/product/2885?gclid=CjwKCAjw6djYBRB8EiwAoAF6oUoEUy16wZWjEGsVpxb3Yl7SzwbvgiCFBv7bbxp7MjHCk8kaTDM9SBoCQPoQAvD_BwE)
2. [DHT11 3-pin sensor](https://www.amazon.com/HiLetgo-Temperature-Humidity-Arduino-Raspberry/dp/B01DKC2GQ0/ref=sr_1_1?ie=UTF8&qid=1528212073&sr=8-1&keywords=dht11)

>**NOTE**: This may work for the DHT22 sensor as well, but I have not tested it. [More info about the different types of basic sensors can be found here.](https://learn.adafruit.com/dht/overview?gclid=CjwKCAjw6djYBRB8EiwAoAF6oQPSnMy0Bl5ASzbWRrnwBWxeKdTrbotF1JVhwHolATO3zRphcGmHFBoCL-AQAvD_BwE)

## Software
This was tested using the following software:

- Raspbian 8.0 (jessie)
- Python 2.7.9

>**NOTE**: This may work with other distros and versions of Python, but I have not tested it.

This script is set to pull two important pieces of data from environment variables:

1. [The URL of the endpoint where the data is to be sent](https://github.com/zdeptawa/azure-iot-temp-humidity/blob/master/temp_humidity_logger.py#L17)
2. [The name of the IOT device sending this data](https://github.com/zdeptawa/azure-iot-temp-humidity/blob/master/temp_humidity_logger.py#L16)

Make sure that you're exporting these prior to running the script! 

>**NOTE**: My RaspberryPi did not see my DHT11 unless I ran this script as root. To use environment variables exported by my underprivileged user, I ran this script with `sudo -E`

For this example, I'm sending my data to a [Microsoft Azure Logic App](https://azure.microsoft.com/en-us/services/logic-apps/) configured to accept this sample schema:

```json
{
  "properties": {
    "epoch": {
      "type": "number"
    },
    "humidity": {
      "type": "number"
    },
    "name": {
      "type": "string"
    },
    "partition_key": {
      "type": "string"
    },
    "temp": {
      "type": "number"
    }
  },
  "type": "object"
}
```

You can check out this [sample_object.json](sample_object.json) file to see a sample payload this script will send in its current form. You don't have to send your data to Azure, but you will need to make sure wherever you're sending it that the mapping/schema is configured properly.