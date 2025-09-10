from seed import connect_to_prodev

def stream_users():
    connection = connect_to_prodev()

    if not connection:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            yield row
    finally:
        cursor.close()
        connection.close()
