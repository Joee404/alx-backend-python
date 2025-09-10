#!/usr/bin/python3
from seed import connect_to_prodev, create_table, insert_data, load_csv_data

connection = connect_to_prodev()
create_table(connection)

data = load_csv_data("user_data.csv")
insert_data(connection, data)

connection.close()
