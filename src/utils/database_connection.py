from os import getenv
import sqlite3
from subprocess import check_output


def get_project_root():
    return check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()


TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DB_PATH = get_project_root()+'/databases/'+getenv('MODE').lower()+'.db'


class DatabaseConnection:
    def __init__(self):
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    def connect(self) -> None:
        if not self.connection:
            self.connection = sqlite3.connect(DB_PATH)
        if not self.cursor:
            self.cursor = self.connection.cursor()
    
    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.connection.commit()
        self.disconnect()
