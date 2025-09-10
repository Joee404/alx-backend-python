#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """Generator that yields ages of users one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:  # yields rows lazily
            yield row["age"]  # only stream age
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    """Calculates average age using the generator without loading all data."""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 1
        total_age += int(age)
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
