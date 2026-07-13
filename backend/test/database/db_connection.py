import psycopg
from dotenv import load_dotenv
load_dotenv()
import os

DATABASE_URL = os.getenv("DATABASE_URI") 
print("fetching database url from .env file")
print("Database URL:", DATABASE_URL[:5])  # Debugging line to check the value of DATABASE_URL

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print(cur.fetchone())