import unittest
import json
import time
##
## unit under test
from zigbeedevice import ActuatorDevice

std_cmds = {'TurnOn' : json.dumps({'on': True }), 'TurnOff': json.dumps({'on': False})}

class UT_1_Construct(unittest.TestCase):
    def test_01_nominal(self):
        uut = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                             deviceID='3')
        
        self.assertEqual(uut.api_path, 'http://127.0.0.1:80/api/611800078A/lights/3')
        self.assertEqual(uut.deviceID, '3')
        self.assertEqual(uut.commands, std_cmds)
        
    def test_02_invalid_deviceID(self):
        uut = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                             deviceID='0')
        
        self.assertEqual(uut.api_path, 'http://127.0.0.1:80/api/611800078A/lights/0')
        self.assertEqual(uut.deviceID, '0')
        self.assertIsNone(uut.commands)
        
    def test_02_invalid_baseURL(self):
        uut = ActuatorDevice(baseURL='http://127.0.0.1:80/api/1234567890/',
                             deviceID='3')
        
        self.assertEqual(uut.api_path, 'http://127.0.0.1:80/api/1234567890/lights/3')
        self.assertEqual(uut.deviceID, '3')
        self.assertIsNone(uut.commands)
        

class UT_2_Command(unittest.TestCase):
    def test_01_nominal_on(self):
        uut = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                             deviceID='4')
        uut.Command('TurnOn')
        time.sleep(2)
        self.assertTrue(uut.IsOn())

    def test_02_nominal_off(self):
        uut = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                             deviceID='4')
        uut.Command('TurnOff')
        time.sleep(2)
        self.assertFalse(uut.IsOn())


if __name__ == '__main__':
    unittest.main()
