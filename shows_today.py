from datetime import date
from datetime import datetime

from database import DataOperations


def main():
    database = DataOperations()
    database.create_db()

    today = datetime.strftime(date.today(), '%A')
    print today
    
    database.search_today(today)

main()
