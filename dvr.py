#!/bin/python2

from database import DataOperations
from database import APICalls

import sys

def print_table(rows):
    if rows == None:
        return
    
    print "\n| %3s | %28s | %8s | %23s | %13s | %13s | %13s |" % ('id', 'name',
                                                  'show_id', 'network',
                                                                  'day', 'season_premiere', 'season_finale')
    print "|-----+------------------------------+----------+-------------------------+---------------+-----------------+---------------|"
    for row in rows:
        print "|%4d | %28s | %8d | %23s | %13s | %15s | %13s |" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        print "|-----+------------------------------+----------+-------------------------+---------------+-----------------+---------------|"
        
    print "\n"

def query(search):
    nw = ""
    
    for string in search:
        nw += string + " "
        
    return nw

def add_entry(query, database):
    api = APICalls()
    
    tuple_show = api.search_show(query, True)
    
    if tuple_show != None:
        season = api.season_premiere(tuple_show[1])
        
        if season != None:
            if database.duplicate(tuple_show[0], tuple_show[1]) == False:
                database.insert_entry(tuple_show[0], tuple_show[1], tuple_show[2], tuple_show[3], season[0], season[1])
                print "\nInserted row [" + tuple_show[0] + ", " + str(tuple_show[1]) + ", " + tuple_show[2] + ", " + tuple_show[3] + ", " + season[0] + ", " + season[1] + "]"
            else:
                print "\nYou must have short term memory because you've already added that show. OOPS!\nThis was totally your fault by the way."
    
    print_table(database.all_rows())

# TODO: handle search queries of names
def remove_entry(database, query="", identification=0):
    database.remove_entry(query, identification)
    print_table(database.all_rows())

def search(query):
    api = APICalls()
    api.search_show(query, False)

def clear_table(database):
    database.remove_db()

def get_help():
    print "\t\t\tOptions"
    print "-i <search term>\t\t\tAdd a show to your list"
    print "\n-ri <identification>\t\t\tRemove a show from your list"
    print "\n-l \t\t\t\t\tList your shows"
    print "\n-s <search term>\t\t\tOnly search for a show. Does not add to your list"
    print "\n-c \t\t\t\t\tClears all of your shows"
    
def flags(flag, database):
    if flag == '-i':
        add_entry(sys.argv[2:], database)
    elif flag == '-r':
        remove_entry(database, query(sys.argv[2:]))
    elif flag == '-ri':
        remove_entry(database, "", sys.argv[2])
    elif flag == '-l':
        print_table(database.all_rows())
    elif flag == '-s':
        search(sys.argv[2:])
    elif flag == '-c':
        clear_table(database)
    else:
        get_help()

# TODO: fix help
def main():
    database = DataOperations()
    database.create_db()
    
    if len(sys.argv) > 1:
        flags(sys.argv[1], database)
#    else:
#        flags("", None)
    
    database.close_db()

main()
