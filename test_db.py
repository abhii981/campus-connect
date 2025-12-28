import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi",
        database="project1"
    )

    if conn.is_connected():
        print("✅ Connected to MySQL successfully")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")

    print("Tables in database:")
    for table in cursor.fetchall():
        print(table)

except mysql.connector.Error as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔒 Connection closed")
