#!/usr/bin/env python3
import unittest
import logging
from plugpwrmgr import *

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
    def __init__(self, initial_state, responsive = True):
        self._state = initial_state
        self._responsive = responsive
    @property
    def state(self):
        return self._state
    def turn_on(self):
        if self._responsive:
            self._state = SmartPlugDummy.ON
    def turn_off(self):
        if self._responsive:
            self._state = SmartPlugDummy.OFF

class PowerWatcherDummy:
    def __init__(self):
        self._messages = []
    def notify_event(self, event_message):
        self._messages.append(event_message)
    @property
    def messages(self):
        return self._messages

class PlugPowerManagerTest(unittest.TestCase):
    def test_schedule_off_plug_off(self):
        plug = SmartPlugDummy(SmartPlugDummy.OFF)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.OFF)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.OFF)
        self.assertTrue(len(watcher.messages) == 0)

    def test_schedule_off_plug_on(self):
        plug = SmartPlugDummy(SmartPlugDummy.ON)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.OFF)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.OFF)
        self.assertTrue(TURNED_OFF_MESSAGE in watcher.messages)

    def test_schedule_on_plug_off(self):
        plug = SmartPlugDummy(SmartPlugDummy.OFF)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.ON)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.ON)
        self.assertTrue(TURNED_ON_MESSAGE in watcher.messages)

    def test_schedule_on_plug_on(self):
        plug = SmartPlugDummy(SmartPlugDummy.ON)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.ON)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.ON)
        self.assertTrue(len(watcher.messages) == 0)

    def test_schedule_off_plug_on_nonresponsive(self):
        plug = SmartPlugDummy(SmartPlugDummy.ON, False)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.OFF)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.ON)
        self.assertTrue(CANNOT_TURN_OFF_MESSAGE in watcher.messages)

    def test_schedule_on_plug_off_nonresponsive(self):
        plug = SmartPlugDummy(SmartPlugDummy.OFF, False)
        schedule = PlugPowerSchduleDummy(PlugPowerSchduleDummy.ON)
        watcher = PowerWatcherDummy()
        manager = PlugPowerManager(schedule, plug, watcher)

        manager.apply_schedule()

        self.assertEqual(plug.state, plug.OFF)
        self.assertTrue(CANNOT_TURN_ON_MESSAGE in watcher.messages)

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()