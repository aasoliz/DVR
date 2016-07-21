from datetime import date
import sqlite3

class DataOperations(object):
    def __init__(self):
        self.name = 'Database'
        self.created = None
        self.connection = None
        self.cursor = None
    
    def create_db(self):
        conn = sqlite3.connect('datatv.db')
        
        c = conn.cursor()
        check = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tvshows'")
        
        if check.fetchone() == None:
            c.execute("CREATE TABLE tvshows (id INTEGER PRIMARY KEY ASC, name TEXT, identification INTEGER, network TEXT, days TEXT, season_premiere TEXT, season_finale TEXT)")
            self.created = date.today()

        self.connection = conn
        self.cursor = c

    def remove_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS tvshows")
        
    def close_db(self):
        self.connection.close()
        
    # TODO: Need to check two shows have the same name
    def remove_entry(self, name, identification):
        self.cursor.execute("DELETE FROM tvshows WHERE identification=(?) OR name=(?)", (identification, name))
        self.connection.commit()

    # TODO: add support for multiple days
    def insert_entry(self, name, identification, network, days, premiere, enddate):
        self.cursor.execute("INSERT INTO tvshows(name, identification, network, days, season_premiere, season_finale) VALUES (?, ?, ?, ?, ?, ?)",
                          (name, identification, network, days, premiere, enddate))
        self.connection.commit()

    def duplicate(self, name, identification):
        row = self.cursor.execute("SELECT * FROM tvshows WHERE identification=(?) AND name=(?)", (identification, name))
        
        if row.fetchone() != None:
            return True
        
        return False

    def search_today(self, day):
        return self.cursor.execute("SELECT * FROM tvshows WHERE days=(?) OR identification=(?)", (day, 3))

    def all_rows(self):
        return self.cursor.execute("SELECT * FROM tvshows")
