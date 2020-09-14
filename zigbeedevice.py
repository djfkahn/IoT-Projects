
import requests
import json

API_KEY = '611800078A'

class ZigBeeDevice():
    
    def __init__(self, baseURL, deviceID, deviceType):
        self.api_path = baseURL + deviceType + '/' + deviceID
        self.deviceID = deviceID
        ##
        ## raise NameError exception if cannot successfully read device
        if not self.Read():
            print('Cannot initiate device with API path of', self.api_path)
            raise NameError

    def Read(self):
        r = requests.get(url = self.api_path)
        if r.ok:
            return json.loads(r.text)
        else:
            return None

    def UpdateBase(self, read_values):
        self.etag     = read_values['etag']
        self.modelid  = read_values['modelid']
        self.name     = read_values['name']
        self.state    = read_values['state']
        self.sw_ver   = read_values['swversion']
        self.type     = read_values['type']
        self.uid      = read_values['uniqueid']
        self.mfr_name = read_values['manufacturername']


class ActuatorDevice(ZigBeeDevice):
    
    def __init__(self, baseURL, deviceID):
        super(ActuatorDevice, self).__init__(baseURL, deviceID, 'lights')
        self.Update()
        self.commands = {'TurnOn' : json.dumps({'on': True }),
                         'TurnOff': json.dumps({'on': False})}

    def Update(self):
        temp               = self.Read()
        self.UpdateBase(temp)
        self.hascolor      = temp['hascolor']
        self.lastannounced = temp['lastannounced']
        self.lastseen      = temp['lastseen']

    def Command(self, cmd):
        put_response = requests.put(url=self.api_path, data=cmd)
        if put_response.ok:
            print('Put', cmd, 'command to the', self.name, 'succeeded.')
        else:
            print('Put', cmd, 'command to the', self.name, 'failed.')

    def IsOn(self):
        return self.Read()['state']['on']

    def IsReachable(self):
        return self.Read()['state']['reachable']

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
        