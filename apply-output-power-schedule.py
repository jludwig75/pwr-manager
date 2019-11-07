#!/usr/bin/env python3
from plugpwrmgr import PlugPowerManager
from powerschedule import SimplePowerSchedule
from emailwatcher import EmailWatcher
import logging
import sys
import os

ROOT_SETTINGS_PATH = '/etc/pwr-manager'
ROOT_LOG_PATH = '/var/log'
POWER_SCHEDULE_FILE = 'power-schedule.json'
GMAIL_SETTINGS_FILE = 'gmail_settings.json'
NOTIFICATION_EMAIL_ADDRESS = 'jr.ludwig@gmail.com'

def settings_path(path):
    if os.geteuid() == 0:
        return os.path.join(ROOT_SETTINGS_PATH, path)
    else:
        return os.path.join(os.path.dirname(sys.argv[0]), path)

def log_path(path):
    if os.geteuid() == 0:
        return os.path.join(ROOT_LOG_PATH, path)
    else:
        return os.path.join(os.path.dirname(sys.argv[0]), path)

class SmartPlugDummy:
    def __init__(self, initial_state):
        self._state = initial_state
    @property
    def state(self):
        return self._state
    def turn_on(self):
        self._state = 'ON'
    def turn_off(self):
        self._state = 'OFF'

if __name__ == '__main__':
    logging.basicConfig(filename=log_path('powermgr.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s %(process)d %(levelname)-8s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    plug = SmartPlugDummy('ON')
    plug.ON = 'ON'
    plug.OFF = 'OFF'
    schedule = SimplePowerSchedule(settings_path(POWER_SCHEDULE_FILE))
    watcher = EmailWatcher(settings_path(GMAIL_SETTINGS_FILE), NOTIFICATION_EMAIL_ADDRESS)

    manager = PlugPowerManager(schedule, plug, watcher)

    manager.apply_schedule()
