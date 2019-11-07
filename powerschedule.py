from datetime import datetime
import json

_DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

"""
Expected schedule format:
{
    "days_of_week": ["Sat", "Sun"],
    "hours_of_day": [0, 1, 2, 3, 4, 5, 6, 20, 21, 22, 23],
    "days_of_month": [1, 15]
}
All schedules that have a value are "anded" together.
All empty schedules are ignored. If all schedules are
empty, the plug will always be on.
Slightly more complex example (first Saturday of every month):
{
    "days_of_week": ["Sat"],
    "hours_of_day": [],
    "days_of_month": [1, 2, 3, 4, 5, 6, 7]
}
All three can be combined (first Saturday of every month during day):
{
    "days_of_week": ["Sat"],
    "hours_of_day": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "days_of_month": [1, 2, 3, 4, 5, 6, 7]
}
"""
class SimplePowerSchedule:
    class _RealClock:
        def get_datetime(self):
            return datetime.now()

    ON = 'ON'
    OFF = 'OFF'

    def __init__(self, schedule_file_path, clock = _RealClock()):
        with open(schedule_file_path, 'r') as sched_file:
            sched_data = sched_file.read()
        self._sched = json.loads(sched_data)
        self._clock = clock

    @property
    def expected_state(self):
        now = self._clock.get_datetime()

        # If the schedule contains days of the week
        if len(self._sched['days_of_week']) > 0:
            # make sure the current day of the week is listed in the schedule
            day = _DAY_NAMES[now.weekday()]
            if not day in self._sched['days_of_week']:
                return SimplePowerSchedule.OFF

        # If the schedule contains days of the month
        if len(self._sched['days_of_month']) > 0:
            # make sure the current day of the month is listed in the schedule
            if not now.day in self._sched['days_of_month']:
                return SimplePowerSchedule.OFF

        # If the schedule contains hours of the day
        if len(self._sched['hours_of_day']) > 0:
            # make sure the current hour of the day is listed in the schedule
            if not now.hour in self._sched['hours_of_day']:
                return SimplePowerSchedule.OFF

        return SimplePowerSchedule.ON
