import logging

TURNED_ON_MESSAGE = 'plug turned on'
TURNED_OFF_MESSAGE = 'plug turned off'
CANNOT_TURN_ON_MESSAGE = 'cannot turn plug on'
CANNOT_TURN_OFF_MESSAGE = 'cannot turn plug off'

class PlugPowerManager:
    def __init__(self, schedule, plug, watcher):
        self._schedule = schedule
        self._plug = plug
        self._watcher = watcher

    def apply_schedule(self):
        logging.info('Applying power schedule')
        try:
            expected_state = self._schedule.expected_state
            logging.info('Expected power state: "%s"' % expected_state)
            if expected_state == self._schedule.ON:
                logging.info('Plug power should be on')
                if self._plug.state == self._plug.OFF:
                    logging.info('Plug should be on, but is off. Turning plug on')
                    self._plug.turn_on()
                    if self._plug.state != self._plug.ON:
                        assert self._plug.state == self._plug.OFF
                        logging.error("Unable to turn plug on")
                        self._watcher.notify_event(CANNOT_TURN_ON_MESSAGE)
                    else:
                        logging.info("plug was successfully turned on")
                        self._watcher.notify_event(TURNED_ON_MESSAGE)
                else:
                    assert self._plug.state == self._schedule.ON
                    logging.info("Plug is already on")
            else:
                assert expected_state == self._schedule.OFF
                logging.info('plug power should be off')
                if self._plug.state == self._plug.ON:
                    logging.info('Plug should be off, but is on. Turning plug off')
                    self._plug.turn_off()
                    if self._plug.state != self._plug.OFF:
                        assert self._plug.state == self._plug.ON
                        logging.error("Unable to turn plug off")
                        self._watcher.notify_event(CANNOT_TURN_OFF_MESSAGE)
                    else:
                        logging.info("plug was successfully turned off")
                        self._watcher.notify_event(TURNED_OFF_MESSAGE)
                else:
                    assert self._plug.state == self._schedule.OFF
                    logging.info("Plug is already off")
        except Exception as e:
            logging.error('Exception applying power schedule: %s' % e)
            raise
