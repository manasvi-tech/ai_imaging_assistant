# Create backend/app/db_test.py
import psycopg2
try:
    conn = psycopg2.connect(
        host="localhost",
        database="medical_db",
        user="postgres",
        password="postgre"  # Replace with your actual password
    )
    print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)