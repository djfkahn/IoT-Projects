import build_device_list

def FindLightBulbs(actuators):
    lightBulbList = []
    for device in actuators:
        if 'light' in device.GetName().lower() or 'bulb' in device.GetName().lower():
            lightBulbList.append(device)
    return lightBulbList
