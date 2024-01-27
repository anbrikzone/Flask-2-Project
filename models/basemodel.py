import sqlite3

class BaseModel():

    def __init__(self) -> None:
        self.connection = sqlite3.connect(database="database/db.sqlite")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        sql = '''
            create table if not exists employees (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                salary REAL
            )
            '''
        self.cursor.execute(sql)
        self.connection.commit()

    

        