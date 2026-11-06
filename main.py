import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent

# Load MySQL credentials from .env
load_dotenv(BASE_DIR / ".env", override=True)

# Create the FastAPI application
app = FastAPI()

# Allow FastAPI to load CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR),
    name="static"
)

# Display the .receipts homepage
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


# Connect to MySQL and retrieve the message
@app.get("/api/poc")
def test_connection():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            use_pure=True
        )

        # Create a database cursor
        cursor = connection.cursor()

        # Retrieve a message from MySQL
        cursor.execute(
            "SELECT message_text FROM messages ORDER BY id LIMIT 1"
        )

        # Get the first result
        row = cursor.fetchone()

        # Check if a message exists
        if row is None:
            raise HTTPException(
                status_code=404,
                detail="No message found in the database."
            )

        # Return the message to the frontend
        return {
            "message": row[0]
        }

    except mysql.connector.Error as error:
        print("MySQL Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to connect to the database."
        )

    finally:
        # Close the cursor
        if cursor is not None:
            cursor.close()

        # Close the database connection
        if connection is not None and connection.is_connected():
            connection.close()
