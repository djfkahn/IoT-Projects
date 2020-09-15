
import requests
import json

API_KEY = '611800078A'

class ZigBeeDevice():
    
    def __init__(self, baseURL, deviceID, deviceType):
        self.api_path = baseURL + deviceType + '/' + deviceID
        self.deviceID = deviceID

    def Read(self):
        r = requests.get(url = self.api_path)
        if r.ok:
            print('Successful GET command from', self.api_path)
            self.last_read = json.loads(r.text)
        else:
            ##
            ## raise NameError exception if cannot successfully read device
            print('Failed GET command from', self.api_path)
            raise NameError

    def UpdateBase(self):
        self.etag     = self.last_read['etag']
        self.modelid  = self.last_read['modelid']
        self.name     = self.last_read['name']
        self.state    = self.last_read['state']
        self.sw_ver   = self.last_read['swversion']
        self.type     = self.last_read['type']
        self.uid      = self.last_read['uniqueid']
        self.mfr_name = self.last_read['manufacturername']


class ActuatorDevice(ZigBeeDevice):
    
    def __init__(self, baseURL, deviceID):
        super(ActuatorDevice, self).__init__(baseURL, deviceID, 'lights')
        self.Update()
        self.commands = {'TurnOn' : json.dumps({'on': True }),
                         'TurnOff': json.dumps({'on': False})}

    def Update(self):
        self.Read()
        self.UpdateBase()
        self.hascolor      = self.last_read['hascolor']
        self.lastannounced = self.last_read['lastannounced']
        self.lastseen      = self.last_read['lastseen']

    def Command(self, cmd):
        put_response = requests.put(url=self.api_path+'/state',
                                    data=self.commands[cmd])
        if put_response.ok:
            print('Successful PUT', cmd, 'command to the', self.name, '.')
        else:
            print('Failed PUT', cmd, 'command to the', self.name, '.')

    def IsOn(self):
        self.Update()
        return self.state['on']

    def IsReachable(self):
        self.Update()
        return self.state['reachable']

class SensorDevice(ZigBeeDevice):
    
    def __init__(self, baseURL, deviceID):
        super(SensorDevice, self).__init__(baseURL, deviceID, 'sensors')
        self.Update()
        if len(self.state.keys()) > 2 or len(self.state.keys()) < 1:
            print('do not know how to determine the measurement name for sensor', self.deviceID, 'named', self.name)
        elif len(self.state.keys()) == 2:
            ##
            ## assume one is the measurement name and the other is 'lastupdated'
            for key in self.state.keys():
                if key != 'lastupdated':
                    self.measurement = key
        else:
            ##
            ## state has only one member, so it must be the measurement name
            self.measurement = self.state.keys()[0]

    def Update(self):
        temp        = self.Read()
        self.UpdateBase(temp)
        self.config = temp['config']

    def GetMeasurement(self):
        return self.Read()['state'][self.measurement]

    def LastUpdated(self):
        return self.Read()['state']['lastupdated']
        