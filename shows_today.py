#!/bin/python2

from datetime import date
from datetime import datetime

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

from database import DataOperations
from database import APICalls
from dvr import print_table

today = date.today()

def notify(name):
    Notify.init("TV Shows")
        
    show = Notify.Notification.new("DVR", name, "dialog-information")
    show.show()

def check_finale(date):
    finale = datetime.strptime(date, '%Y-%m-%d')
    
    if finale.year == today.year:
        if finale.month > today.month:
            return True
        elif finale.month == today.month:
            if finale.day >= today.day:
                return True
    return False

def episode_aired(identification, date):
    api = APICalls()
    aired = api.episode_list(identification, str(date))
    
    if aired:
        return True
    return False

def main():
    database = DataOperations()
    database.create_db()
    
    day_week = datetime.strftime(today, '%A')
    rows = database.search_today(day_week)
    
    for row in rows:
        running = check_finale(row[6])
        
        if running:
            if episode_aired(row[2], str(today)):
                notify("\t" + row[1])
            else:
                print "\nThe show %s didn't air an episode today. I know how rude!"
        else:
            database.remove_entry("", row[2])
            print "\nThe show's %s season ended. So I did you a favor and removed it for you." % row[2]
        
    print_table(database.search_today(day_week))
    notify('I have graciously put all the information into a file. So You\'re Welcome!')
    
    database.close_db()

main()
