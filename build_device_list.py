import requests
import json
import zigbeedevice

def build_device_lists(APIKEY):
    ##
    ## initialize local variables
    actuator_list = []
    sensor_list   = []

    ##
    ## assume the REST API is hosted locally
    baseURL = 'http://127.0.0.1:80/api/' + APIKEY + '/'

    ##
    ## read all the actuating devices
    actuators_dict = json.loads(requests.get(url=baseURL+'lights').text)
    for deviceID in actuators_dict.keys():
        a_device = zigbeedevice.ActuatorDevice(baseURL, deviceID)
        actuator_list.append(a_device)

    sensors_dict = json.loads(requests.get(url=baseURL+'sensors').text)
    for deviceID in sensors_dict.keys():
        s_device = zigbeedevice.SensorDevice(baseURL, deviceID)
        sensor_list.append(s_device)

    return actuator_list, sensor_list

def main():
    a_list, s_list = build_device_lists('611800078A')
    
    print('Found', len(a_list),'actuators')
    print('Found', len(s_list),'sensors')
    
if __name__ == '__main__':
    main()