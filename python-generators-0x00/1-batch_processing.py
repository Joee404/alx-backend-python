from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            for row in batch:
                yield row
    finally:
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    """Processes batches and filters users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                print(user)
