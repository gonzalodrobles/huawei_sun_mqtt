from datetime import datetime
from huawei_solar import AsyncHuaweiSolar
import asyncio
import json
with open('conf.json', 'r') as f:
    jsonConf = json.load(f)

huaweiHost = jsonConf["huawei"]["host"]
huaweiPort = jsonConf["huawei"]["port"]
huaweiSlave = jsonConf["huawei"]["slave"]
mqtt_broker_address= jsonConf["mqtt"]["broker_address"]
port = jsonConf["mqtt"]["port"]

async def fetchModBus(names, result):
    hs = await AsyncHuaweiSolar.create(huaweiHost, port=huaweiPort, slave=huaweiSlave)
    responses = await hs.get_multiple(names)
    for name, response in zip(names, responses):
        result[name] = response
        #print(f"{name}: {response}")
    await hs.stop()

def getHuaweiData(lCommands,result):
    print("fetching ModBus data...")
    for iCommand in lCommands:
        asyncio.run(fetchModBus(iCommand,result))
    print("ModBus data fetched!")


import paho.mqtt.client as mqttClient
import time
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global mqttConnected                #Use global variable
        mqttConnected = True                #Signal connection
        client.publish("huawei-sun/mqtt_available",1)
    else:
        print("Connection failed")
mqttConnected = False   #global variable for the state of the connection

def publishMQTT(client,result):
    print("Publishing data to MQTT Broker...")
    for name,value in result.items():
        client.publish(jsonConf["mqtt"]['huawei_topic']+"/"+name,str(value[0]))
    print("Data published to MQTT Broker!")

def modbus2MQTT():
    client = mqttClient.Client("huawei_solar")
    if jsonConf["mqtt"]["username"] != "":
        client.username_pw_set(jsonConf["mqtt"]["username"], password=jsonConf["mqtt"]["password"])
    client.will_set("huawei-sun/mqtt_available", payload=0, qos=0, retain=False)
    client.connect(mqtt_broker_address, port=port)
    client.on_connect= on_connect
    client.loop_start()        #start the loop
    while mqttConnected != True:    #Wait for connection
        time.sleep(0.1)
    while True:
        result = {}
        result["last_refresh"] = [datetime.now().strftime('%Y-%m-%d %H:%M:%m')]
        getHuaweiData(jsonConf["lCommands"],result)
        publishMQTT(client,result)
        print("Next data sync on "+str(jsonConf["mqtt"]["topic_refresh"])+" seconds...")
        time.sleep(jsonConf["mqtt"]["topic_refresh"])


if __name__ == '__main__':
    modbus2MQTT()
