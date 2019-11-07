#!/usr/bin/env python3
from plugpwrmgr import PlugPowerManager
from powerschedule import SimplePowerSchedule
from emailwatcher import EmailWatcher
import logging
import sys

POWER_SCHEDULE_FILE = 'power-schedule.json'
NOTIFICATION_EMAIL_ADDRESS = 'jr.ludwig@gmail.com'
GMAIL_SETTINGS_FILE = 'gmail_settings.json'

class SmartPlugDummy:
    ON = 'ON'
    OFF = 'OFF'
    def __init__(self, initial_state):
        self._state = initial_state
    @property
    def state(self):
        return self._state
    def turn_on(self):
        self._state = SmartPlugDummy.ON
    def turn_off(self):
        self._state = SmartPlugDummy.OFF

if __name__ == '__main__':
    logging.basicConfig(filename='powermgr.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(process)d %(levelname)-8s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    plug = SmartPlugDummy(SmartPlugDummy.ON)
    schedule = SimplePowerSchedule(POWER_SCHEDULE_FILE)
    watcher = EmailWatcher(GMAIL_SETTINGS_FILE, GMAIL_SETTINGS_FILE)

    manager = PlugPowerManager(schedule, plug, watcher)

    manager.apply_schedule()
