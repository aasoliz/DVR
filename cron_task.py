#!/bin/python2

from crontab import CronTab

user_cron = CronTab(user='aasoliz')

job = user_cron.new(command='/home/aasoliz/Documents/Projects/DVR/shows_today.py >> /home/aasoliz/Documents/Projects/DVR/current')

job.hour.on(22)
job.day.every(1)

user_cron.write_to_user(user='aasoliz')
print user_cron.render()

assert job.is_valid()
