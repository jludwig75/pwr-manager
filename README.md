# pwr-manager - Manage KASA Smart Plugs

This project is designed to manage a KASA SmartPlug from a Linux server (i.e. Raspberry Pi). The project is designed to be run from an hourly chron job.

To setup:
1. Install the pyHS100 library: sudo pip3 install pyHS100. https://github.com/GadgetReactor/pyHS100
2. Copy mail_settings.template.json to /etc/pwr-manager/mail_settings.json
3. Put mail credentials for the sending account in /etc/pwr-manager/mail_settings.json
4. If you are using gmail, setup the sending gmail account to "Allow less secure apps" (I used a separate gmail account just for sending so I didn't have to set this on my general use account.
5. Copy power-schedule.template.json to /etc/pwr-manager/power-schedule.json
6. Set your desired schedule in /etc/pwr-manager/power-schedule.json. See schedule documentation below.
7. Copy settings.template.json to /etc/pwr-manager/settings.json
8. Put the plug IP address and notification email address in /etc/pwr-manager/settings.json
9. Set up a chron job to run apply-output-power-schedule.py hourly as root.

Schedule Settings
===
Expected schedule format:
```json
{
    "days_of_week": ["Sat", "Sun"],
    "hours_of_day": [0, 1, 2, 3, 4, 5, 6, 20, 21, 22, 23],
    "days_of_month": [1, 15]
}
```
All schedules that have a value are "anded" together. All empty schedules are ignored. If all schedules are empty, the plug will always be on.

Slightly more complex example (first Saturday of every month):
```json
{
    "days_of_week": ["Sat"],
    "hours_of_day": [],
    "days_of_month": [1, 2, 3, 4, 5, 6, 7]
}
```
All three can be combined (first Saturday of every month during day):
```json
{
    "days_of_week": ["Sat"],
    "hours_of_day": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "days_of_month": [1, 2, 3, 4, 5, 6, 7]
}
```
