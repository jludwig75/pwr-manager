#!/usr/bin/env python3
import unittest
import logging
import json
import os
from datetime import datetime
from powerschedule import SimplePowerSchedule

class FixedDummyClock:
    def __init__(self, dt):
        self._dt = dt
    def get_datetime(self):
        return self._dt
    def set_datetime(self, dt):
        self._dt = dt

class SimplePowerScheduleTest(unittest.TestCase):
    def _gen_sched_file(self, file_name, days_of_week = [], hours_of_day = [], days_of_month = []):
        sched = {'days_of_week': days_of_week, 'hours_of_day': hours_of_day, 'days_of_month': days_of_month}
        with open(file_name, 'wt') as sched_file:
            sched_file.write(json.dumps(sched))

    def test_day_of_the_week(self):
        TEST_SCHED_FILE_NAME = 'test-sched1.json'
        self._gen_sched_file(TEST_SCHED_FILE_NAME, days_of_week = ['Tue', 'Thu', 'Fri'])
        dt = datetime(2019, 11, day=4)
        assert dt.weekday() == 0
        clock = FixedDummyClock(dt)

        sched = SimplePowerSchedule(TEST_SCHED_FILE_NAME, clock)
        os.unlink(TEST_SCHED_FILE_NAME)

        # Day 0 - Monday
        clock.set_datetime(datetime(2019, 11, day=4))
        self.assertEqual(sched.expected_state, sched.OFF)

        # Day 0 - Tuesday
        clock.set_datetime(datetime(2019, 11, day=5))
        self.assertEqual(sched.expected_state, sched.ON)

        # Day 0 - Wednesday
        clock.set_datetime(datetime(2019, 11, day=6))
        self.assertEqual(sched.expected_state, sched.OFF)

        # Day 0 - Thursday
        clock.set_datetime(datetime(2019, 11, day=7))
        self.assertEqual(sched.expected_state, sched.ON)

        # Day 0 - Friday
        clock.set_datetime(datetime(2019, 11, day=8))
        self.assertEqual(sched.expected_state, sched.ON)

        # Day 0 - Saturday
        clock.set_datetime(datetime(2019, 11, day=9))
        self.assertEqual(sched.expected_state, sched.OFF)

        # Day 0 - Sunday
        clock.set_datetime(datetime(2019, 11, day=10))
        self.assertEqual(sched.expected_state, sched.OFF)
        

    def test_hour_of_the_day(self):
        TEST_SCHED_FILE_NAME = 'test-sched2.json'
        self._gen_sched_file(TEST_SCHED_FILE_NAME, hours_of_day = [6, 7, 8, 16, 17])
        dt = datetime(2019, 11, day=7, hour=5)
        clock = FixedDummyClock(dt)

        sched = SimplePowerSchedule(TEST_SCHED_FILE_NAME, clock)
        os.unlink(TEST_SCHED_FILE_NAME)

        clock.set_datetime(datetime(2019, 11, 7, hour=0))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, 7, hour=5))
        self.assertEqual(sched.expected_state, sched.OFF)
        clock.set_datetime(datetime(2019, 11, 7, hour=6))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, 7, hour=7))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, 7, hour=8))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, 7, hour=9))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, 7, hour=15))
        self.assertEqual(sched.expected_state, sched.OFF)
        clock.set_datetime(datetime(2019, 11, 7, hour=16))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, 7, hour=17))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, 7, hour=18))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, 7, hour=23))
        self.assertEqual(sched.expected_state, sched.OFF)

    def test_day_of_the_month(self):
        TEST_SCHED_FILE_NAME = 'test-sched3.json'
        self._gen_sched_file(TEST_SCHED_FILE_NAME, days_of_month = [7, 8, 17])
        dt = datetime(2019, 11, day=6)
        clock = FixedDummyClock(dt)

        sched = SimplePowerSchedule(TEST_SCHED_FILE_NAME, clock)
        os.unlink(TEST_SCHED_FILE_NAME)

        clock.set_datetime(datetime(2019, 11, day=1))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, day=6))
        self.assertEqual(sched.expected_state, sched.OFF)
        clock.set_datetime(datetime(2019, 11, day=7))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, day=8))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, day=9))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, day=16))
        self.assertEqual(sched.expected_state, sched.OFF)
        clock.set_datetime(datetime(2019, 11, day=17))
        self.assertEqual(sched.expected_state, sched.ON)
        clock.set_datetime(datetime(2019, 11, day=18))
        self.assertEqual(sched.expected_state, sched.OFF)

        clock.set_datetime(datetime(2019, 11, day=30))
        self.assertEqual(sched.expected_state, sched.OFF)

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()