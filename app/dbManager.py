import sqlite3


def add_entry(event_date, event_time, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10):
    sqliteConnection = sqlite3.connect('sensor_data.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS sensor_output (
                                       date timestamp,
                                       time timestamp,
                                       d1 REAL,
                                       d2 REAL,
                                       d3 REAL,
                                       d4 REAL,
                                       d5 REAL,
                                       d6 REAL,
                                       d7 REAL,
                                       d8 REAL,
                                       d9 REAL,
                                       d10 REAL);'''

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_create_table_query)

    sqlite_insert_with_param = """INSERT INTO 'sensor_output'
                          ('date', 'time', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10') 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    data_tuple = (event_date, event_time, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def get_all_entries():
    sqliteConnection = sqlite3.connect('sensor_data.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_query = """SELECT * FROM sensor_output"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()
    return records


def get_entries_from_date(date):
    sqliteConnection = sqlite3.connect('sensor_data.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM sensor_output WHERE date= ?"
    cursor.execute(sqlite_select_query, (date,))
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()

    return records


def get_entries_date_range(start, stop):
    sqliteConnection = sqlite3.connect('sensor_data.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM sensor_output WHERE date >= ? AND date <= ?"
    cursor.execute(sqlite_select_query, (start, stop,))
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()

    return records


if __name__ == "__main__":
    # add_entry('2021-3-22', '13:37:00', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    print(get_all_entries())
    #print(get_entries_from_date('2021-3-22'))
    # get_entries_date_range(start='2021-3-19', stop='2021-3-21')