# Developed by @sanuja : https://github.com/sanuja-gayantha

import sqlite3
import os


class Database():

    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(os.getcwd(), './database/database.db'))
        self.cur = self.connection.cursor()


    # https://codereview.stackexchange.com/questions/182700/python-class-to-manage-a-table-in-sqlite
    def __enter__(self):
        return self


    def __exit__(self, ext_type, exc_value, exc_traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


    def create_table_urls(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TEMP_URLS(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    VALID_URL VARCHAR,
                                                                    STATUS VARCHAR);''')
    def drop_table_urls(self):
        self.cur.execute("DROP TABLE TEMP_URLS") 

    def append_to_table_urls(self, table_url, table_ststus):
        self.cur.execute('''INSERT INTO TEMP_URLS (VALID_URL, STATUS) VALUES (?, ?)''', (table_url, table_ststus,))

    

    def create_table_pdf_urls(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TEMP_PDF_URLS(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    VALID_PDF_URL VARCHAR);''')
