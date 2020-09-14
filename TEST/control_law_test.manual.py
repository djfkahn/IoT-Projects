import unittest
from zigbeedevice import ActuatorDevice
##
## unit under test
from control_law import ManualControlLaw

class UT_Construct(unittest.TestCase):
    def test_01_nominal(self):
        test_actuator = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                                       deviceID='3')
        uut = ManualControlLaw(test_actuator, 21)
        
        self.assertIsNone(uut.sensor)
        self.assertEqual(uut.actuator, test_actuator)
        self.assertFalse(uut.is_manually_on)
        self.assertFalse(uut.is_manually_off)
        
    def test_02_invalid_deviceID(self):
        test_actuator = ActuatorDevice(baseURL='http://127.0.0.1:80/api/611800078A/',
                                       deviceID='0')
        uut = ManualControlLaw(test_actuator, 21)
        
        self.assertIsNone(uut.sensor)
        self.assertEqual(uut.actuator, test_actuator)
        self.assertFalse(uut.is_manually_on)
        self.assertFalse(uut.is_manually_off)
        
    def test_02_invalid_baseURL(self):
        test_actuator = ActuatorDevice(baseURL='http://127.0.0.1:80/api/1234567890/',
                                       deviceID='3')
        uut = ManualControlLaw(test_actuator, 21)
        
        self.assertIsNone(uut.sensor)
        self.assertEqual(uut.actuator, test_actuator)
        self.assertFalse(uut.is_manually_on)
        self.assertFalse(uut.is_manually_off)
        
if __name__ == '__main__':
    unittest.main()