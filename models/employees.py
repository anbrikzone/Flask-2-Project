import sqlite3
from models.basemodel import BaseModel

class Employee(BaseModel):

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