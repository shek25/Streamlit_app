import sqlite3
# Establish a connection to the database
conn = sqlite3.connect('my_database.sqlite3')
# Create a cursor object using the cursor() method
cursor = conn.cursor()
# SQL command to create a table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);'''
# Execute the SQL command
cursor.execute(create_table_sql)
# Commit the changes
conn.commit()  
# Close the connection
conn.close()
