# imports for ManualControlLaw
import RPi.GPIO as GPIO
from gpiozero import Button

# imports for SunsetToSunriseControlLaw
import requests
import json

# imports used in several ControlLaws
from datetime import datetime, date, time, timezone
from utils import ComputeSecInDay


class ControlLaw():
    def __init__(self, sensor, actuator):
        self.sensor   = sensor
        self.actuator = actuator
        

class ManualControlLaw(ControlLaw):
    def __init__(self, actuator, GPIOpin):
        super(ManualControlLaw, self).__init__(None, actuator)
        self.button          = Button(GPIOpin)
        self.is_manually_on  = False
        self.is_manually_off = False

    def IsManuallyControlled(self):
        return self.is_manually_on or self.is_manually_off

    def Control(self):
        ##
        ## only control if the actuator is not reachable
        if self.actuator.IsReachable():
            ##
            ## determine if the button is pressed, and
            ## set up command based on current state
            if self.button.is_pressed:
                ##
                ## check whether the actuator is already on
                if self.actuator.IsOn():
                    ##
                    ## actuator is already on, so the command is to turn it off
                    cmd = 'TurnOff'
                    ##
                    ## set manual flags based on whether the actuator was on
                    ## due to autonomous control or manual.
                    if self.is_manually_on:
                        ##
                        ## manually turning off actuator turned on manually, so
                        ## set flag to allow autonomous control to proceed
                        self.is_manually_on  = False
                        self.is_manually_off = False
                    else:
                        ##
                        ## actuator was autonomously turned on, so mark it as
                        ## manually turned off to prevent autonomously turning it
                        ## on again.
                        self.is_manually_off = True
                else:
                    ##
                    ## actuator is off, so the command is to turn it on
                    cmd = 'TurnOn'
                    ##
                    ## set manual control flag to indicate manual control
                    self.is_manually_on  = True
                    self.is_manually_off = False
                ##
                ## send the command
                self.actuator.Command(cmd)


class ScheduleByTimeControlLaw(ControlLaw):
    def __init__(self, actuator, on_times, off_times):
        super(ScheduleByTimeControlLaw, self).__init__(None, actuator)
        self.Update(on_times, off_times)
        
    def Update(self, on_times, off_times):
        if len(on_times) != len(off_times):
            print('Trying to set time-scheduled control law with unequal on and off times')

        self.time_schedule = []
        for x in range(min(len(on_times),len(off_times))):
            self.time_schedule.append({'on': on_times[x], 'off': off_times[x]})

    def Control(self):
        ##
        ## get the current local time, and convert it to seconds into the day
        sec_in_day = ComputeSecInDay(datetime.now())
        ##
        ## if the local seconds into the day falls within a scheduled on-time,
        ## then turn on the actuator.  otherwise, turn it off
        for time_slot in self.time_schedule:
            if time_slot['on'] <= sec_in_day < time_slot['off']:
                ## only send the ON command if the actuator is currently OFF
                if not self.actuator.IsOn():
                    self.actuator.Command('TurnOn')
            else:
                ## only send the OFF command if the actuator is currently ON
                if self.actuator.IsOn():
                    self.actuator.Command('TurnOff')

class SunsetToSunriseControlLaw(ControlLaw):
    def __init__(self, actuator, sunset_offset=0, sunrise_offset=0):
        super(ScheduleByTimeControlLaw, self).__init__(None, actuator)
        self.api_url        = 'https://api.sunrise-sunset.org/json'
        ##
        ## pulled lat and long manually from Google maps
        self.api_params     = {'lat':37.3052272,'lng':-121.9871217}
        self.sunset_offset  = sunset_offset
        self.sunrise_offset = sunrise_offset
        self.Update(sunset_offset, sunrise_offset)

    def ExtractLocalTime(time_str):
        STDOFFSET = timedelta(seconds = -_time.timezone)
        this_time = datetime.strptime(time_str,"%I:%M:%S %p")
        return datetime.combine(datetime.today().date(), this_time.time())-STDOFFSET

    def Update(self):
        r = json.loads(requests.get(url=self.api_url, params=self.api_params))['results']
        self.sunrise_time = ExtractLocalTime(r['sunrise'])
        self.sunset_time  = ExtractLocalTime(r['sunset'])
        self.sunrise_tod  = ComputeSecInDay(self.sunrise_time) + self.sunrise_offset
        self.sunset_tod   = ComputeSecInDay(self.sunset_time) + self.sunset_offset


    def Control(self):
        ##
        ## get the current local time, and convert it to seconds into the day
        sec_in_day = ComputeSecInDay(datetime.now())
        ##
        ## if current time is before sunrise or after sunset, command the actuator
        ## ON.  otherwise, command it OFF.
        if sec_in_day < self.sunrise_tod or sec_in_day > self.sunset_tod:
            ## only send the ON command if the actuator is currently OFF
            if not self.actuator.IsOn():
                self.actuator.Command('TurnOn')
        else:
            ## only send the OFF command if the actuator is currently ON
            if self.actuator.IsOn():
                self.actuator.Command('TurnOff')
            