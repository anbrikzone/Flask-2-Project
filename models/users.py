import sqlite3
from models.basemodel import BaseModel
from flask_login import UserMixin

class Users(UserMixin, BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.table = "users"

    def create(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
        
    def update(self, id, **kwargs):
        try:
            self.cursor.execute(f"UPDATE {self.table} SET first_name = ?, last_name = ?, department = ?, salary=? WHERE id = ?", (list(kwargs.values()), id))
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def remove(self, id):
        try:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE id = {id}")
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def get_all(self):
        try:
            result = self.cursor.execute(f"SELECT * FROM {self.table}").fetchall()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
        
    def get_by_id(self, id):
        try:
            result = self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = {id}").fetchone()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
