import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Posgres Configuration
DB_CONN = psycopg2.connect(
    host="localhost", 
    port=os.getenv("PORT"), 
    user= os.getenv("DB_USER"), 
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
DB_CURSOR = DB_CONN.cursor()



# user = "Chris"
# passwd = "12345"
# date = datetime.now()   

# # Execute the query
# DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS users ( 
#                   username TEXT PRIMARY KEY, 
#                   password TEXT NOT NULL, 
#                   last_login TIMESTAMP NOT NULL)""")

# # Insert the user data safely using parameterized query
# insert_query = "INSERT INTO users (username, password, last_login) VALUES (%s, %s, %s)"
# DB_CURSOR.execute(insert_query, (user, passwd, date))

# # Commit the transaction
# DB_CONN.commit()

# DB_CURSOR.execute("SELECT * FROM users ")
# data = DB_CURSOR.fetchall()

# # Close the cursor and connection
# DB_CURSOR.close()
# DB_CONN.close()


# # Fetch the data
# print(data)
# # Print the result
# for row in data:
#     print(row)

