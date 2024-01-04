import sqlite3

def print_database_data():
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()

    # Execute a query to select all data
    c.execute('SELECT * FROM decisions')

    # Fetch and print all rows of data
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

# Call the function to print data
print_database_data()
