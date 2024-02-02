import sqlite3

class BaseModel():

    def __init__(self) -> None:
        self.connection = sqlite3.connect(database="database/db.sqlite")
        self.cursor = self.connection.cursor()
        self.create_table_users()
        self.create_table_tasks()

    def create_table_users(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            username TEXT,
            password TEXT,
            email    TEXT
        );
            '''
        self.cursor.execute(sql)
        self.connection.commit()

           
    def create_table_tasks(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS tasks (
            id      INTEGER     PRIMARY KEY AUTOINCREMENT UNIQUE,
            title   TEXT,
            status  INTEGER (1),
            user_id INTEGER     REFERENCES users (id)   ON DELETE CASCADE
                                                        ON UPDATE CASCADE
        );
            '''
        self.cursor.execute(sql)
        self.connection.commit()       
           
            
    

        