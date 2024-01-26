import sqlite3
from models.basemodel import BaseModel

class Employees(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.table = "employees"

    def create_employee(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
        
    def update_employee(self, id, first_name, last_name, department, salary):
        try:
            self.cursor.execute(f"UPDATE {self.table} SET first_name = '{first_name}', last_name = '{last_name}', department = '{department}', salary={salary} WHERE id = {id}")
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def get_all_employees(self):
        try:
            result = self.cursor.execute(f"SELECT * FROM {self.table}").fetchall()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0