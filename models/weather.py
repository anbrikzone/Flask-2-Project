import sqlite3
from models.basemodel import BaseModel
from services.weatherapi import WeatherAPI

class Weather(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.table = "weather"

    def create(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
        
    def update(self, location, json):
        try:
            self.cursor.execute(f"UPDATE {self.table} SET json = ?, date_update = strftime('%Y-%m-%d %H:%M:%S','now', 'localtime') WHERE location = ?", (json, location))
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def get_by_location(self, location):
        try:
            result = self.cursor.execute(f"SELECT date_update, json FROM {self.table} WHERE location = ?", (location,)).fetchone()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0