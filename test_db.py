import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

print("Environment file found:", ENV_FILE.is_file())
print("Username loaded:", repr(os.getenv("DB_USER")))
print("Password loaded:", bool(os.getenv("DB_PASSWORD")))

try:
    # Connect Python to MySQL
   
    connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    use_pure=True
)


    print("SUCCESS: Connected to MySQL!")

    # Test the messages table
    cursor = connection.cursor()

    cursor.execute(
        "SELECT message_text FROM messages LIMIT 1"
    )

    result = cursor.fetchone()

    print("Database result:", result)

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("MySQL Error Number:", error.errno)
    print("MySQL Error:", error.msg)
