# pwr-manager - Manage KASA Smart Plugs

This project is designed to manage a KASA SmartPlug from a Linux server (i.e. Raspberry Pi). The project is designed to be run from an hourly chron job.

To setup:
1. Copy gmail_settings.template.json to /etc/pwr-manager/gmail_settings.json
2. Put gmail credentials for the sending account in /etc/pwr-manager/gmail_settings.json
3. Setup the sending gmail account to "Allow less secure apps" (I used a separate gmail account just for sending so I didn't have to set this on my general use account.
4. Copy power-schedule.template.json to /etc/pwr-manager/power-schedule.json
5. Set your desired schedule in /etc/pwr-manager/power-schedule.json. See schedule documentation below.
6. Set up a chron job to run apply-output-power-schedule.py hourly as root.

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
