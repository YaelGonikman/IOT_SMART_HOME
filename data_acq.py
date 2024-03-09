import sqlite3
from datetime import datetime

# Database initialization
def init_db():
    conn = sqlite3.connect('printer_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS printer_logs (
            timestamp TEXT,
            ink_amount REAL,
            pages_printed INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to add printer data to the database
def add_printer_data(ink_amount, pages_printed):
    timestamp = str(datetime.now())
    conn = sqlite3.connect('printer_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO printer_logs (timestamp, ink_amount, pages_printed)
        VALUES (?, ?, ?)
    ''', (timestamp, ink_amount, pages_printed))
    conn.commit()
    conn.close()


def print_all_printer_data():
    conn = sqlite3.connect('printer_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM printer_logs')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

# if __name__ == '__main__':
    # init if not intiated
    # init_db() 
    # Seed demo data
    # add_printer_data(10.5, 50)
    # Show all saved values
    # print_all_printer_data()
