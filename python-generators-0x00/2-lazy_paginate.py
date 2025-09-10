#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator to lazily paginate through user_data"""
    offset = 0
    while True:   # only one loop
        rows = paginate_users(page_size, offset)
        if not rows:   # stop when no more data
            break
        yield rows
        offset += page_size
