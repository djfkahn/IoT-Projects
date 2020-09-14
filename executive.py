import time
from build_device_list import build_device_lists
import periodic

APIKEY = '611800078A'
actuator_list = []
sensor_list   = []
control_laws  = []

def SetUp():
    ##
    ## 1. determine if the APIKEY still works.  if it does not, get a new one.
    
    ##
    ## 2. read the list of actuators and sensors
    actuator_list, sensor_list = build_device_lists(APIKEY)
    ##
    ## 3. connect actuators and sensors to control laws
    pass

def PeriodicProcessing():
    inner_loop_start_time = time.time()
    inner_loop_period     = 10       # = 10 seconds
    mid_loop_start_time   = inner_loop_start_time
    mid_loop_period       = 60  # 60*60    # = 1 hour
    outer_loop_start_time = inner_loop_start_time
    outer_loop_period     = 600 # 24*60*60 # = 1 day

    while True:
        current_time = time.time()
        
        ##
        ## Check if it is time to run the inner loop
        elapsed_time = current_time - inner_loop_start_time
        if elapsed_time > inner_loop_period:
            ##
            ## do inner loop stuff
            print("Performing the inner loop at ", str(current_time))
            periodic.DoInnerLoop()
            
            ##
            ## reset the inner loop start time
            inner_loop_start_time = current_time

        ##
        ## Check if it is time to run the mid loop
        elapsed_time = current_time - mid_loop_start_time
        if elapsed_time > mid_loop_period:
            ##
            ## do mid loop stuff
            print("Performing the middle loop at ", str(current_time))
            periodic.DoMidLoop()
            
            ##
            ## reset the mid loop start time
            mid_loop_start_time = current_time

        ##
        ## Check if it is time to run the outer loop
        elapsed_time = current_time - outer_loop_start_time
        if elapsed_time > outer_loop_period:
            ##
            ## do outer loop stuff
            print("Performing the outer loop at ", str(current_time))
            periodic.DoOuterLoop()
            
            ##
            ## reset the inner loop start time
            outer_loop_start_time = current_time

def Executive():
    ##
    ## run the set up
    SetUp()
    ##
    ## run the periodic processing
    try:
        PeriodicProcessing()
        
    except KeyboardInterrupt:
        print('\nCtrl-C pressed!  Program will turn off all the actuators and exit.')
        for device in actuator_list:
            device.Command('TurnOff')
            
        print('Done.  Goodbye.')
    
if __name__ == '__main__':
    Executive()