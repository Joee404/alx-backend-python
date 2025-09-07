import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="alx_user",
        password="alx_pass",
        database="mysql"
    )
    print("✅ Connection successful")
    conn.close()
except Exception as e:
    print("❌ Error:", e)
