#!/usr/bin/env python3
from plugpwrmgr import *
import logging
import sys

class PlugPowerSchduleDummy:
    ON = 'ON'
    OFF = 'OFF'
    def __init__(self, expected_state):
        self._expected_state = expected_state
    @property
    def expected_state(self):
        return self._expected_state

class SmartPlugDummy:
    ON = 'ON'
    OFF = 'OFF'
    def __init__(self, name, initial_state):
        self._state = initial_state
    @property
    def state(self):
        return self._state
    def turn_on(self):
        self._state = SmartPlugDummy.ON
    def turn_off(self):
        self._state = SmartPlugDummy.OFF

class PowerWatcherDummy:
    def __init__(self):
        self._messages = []
    def notify_event(self, event_message):
        self._messages.append(event_message)

logging.basicConfig(filename='powermgr.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(process)d %(levelname)-8s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

plug = SmartPlugDummy('172.18.1.41', SmartPlugDummy.OFF)
schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.ON)
watcher = PowerWatcherDummy()

manager = PlugPowerManager(schedule, plug, watcher)

manager.apply_schedule()

