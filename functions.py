import mysql.connector
from faker import Faker
import random
from config import db_config
import os
import subprocess


def mysql_connection(config):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["password"],
            database=config["database"]
        )
        print("MySQL Database connection successful")
    except mysql.connector.Error as err:
        print('Something went wrong: {}'.format(err))
    return connection


connection = mysql_connection(db_config)


def pop_users():

    fake = Faker()
    cursor = connection.cursor()
    user_iden = 0
    type_list = ['admin', 'employee', 'customer']

    for _ in range(1000):

        user_iden += 1
        user_id = user_iden
        full_name = fake.name()
        email = fake.unique.email()
        password_hash = fake.password()
        user_type = random.choice(type_list)
        cursor.execute('INSERT INTO users (user_id, full_name, email, password_hash, user_type) VALUES (%s, %s, %s, %s, %s)',
                       (user_id, full_name, email, password_hash, user_type))

    connection.commit()
    cursor.close()
    return


def pop_products():

    fake = Faker()
    cursor = connection.cursor()
    product_iden = 0

    for _ in range(236):

        product_iden += 1
        product_id = product_iden
        product_name = fake.unique.word()
        product_description = fake.sentence()
        price = round(random.uniform(10, 500), 2)
        stock = round(random.uniform(10, 500), None)
        cursor.execute('INSERT INTO products (product_id, product_name, product_description, price, stock) VALUES (%s, %s, %s, %s, %s)',
                       (product_id, product_name, product_description, price, stock))

    connection.commit()
    cursor.close()
    return


def pop_orders():

    fake = Faker()
    cursor = connection.cursor()
    order_iden = 0
    status_list = ['pending', 'completed', 'canceled']

    for _ in range(150):

        order_iden += 1
        order_id = order_iden
        user_id = round(random.uniform(1, 1000), None)
        order_date = fake.date()
        status = random.choice(status_list)
        cursor.execute('INSERT INTO orders (order_id, user_id, order_date, status) VALUES (%s, %s, %s, %s)',
                       (order_id, user_id, order_date, status))

    connection.commit()
    cursor.close()
    return


def pop_order_items():

    fake = Faker()
    cursor = connection.cursor()
    item_iden = 0

    for _ in range(150):

        item_iden += 1
        item_id = item_iden
        order_id = round(random.uniform(1, 150), None)
        product_id = round(random.uniform(1, 236), None)
        quantity = round(random.uniform(1, 30), None)
        unit_price = round(random.uniform(200, 1700), 2)
        cursor.execute('INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s, %s)',
                       (item_id, order_id, product_id, quantity, unit_price))

    connection.commit()
    cursor.close()
    return


def create_backup():
    backup_file = "C:/Backup_SQLproject/backup.sql"
    # Caminho completo para mysqldump
    mysqldump_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
    # Comando para criar o backup
    backup_command = f'"{mysqldump_path}" -h {db_config["host"]} -u {db_config["user"]} -p{db_config["password"]} {db_config["database"]} > "{backup_file}"'
    # Executa o backup no CMD
    process = subprocess.run(backup_command, shell=True,
                             capture_output=True, text=True)
    if process.returncode == 0:
        print(f"Backup salvo com sucesso em: {backup_file}")
    else:
        print(f"Erro ao criar backup: {process.stderr}")


def restore_backup():
    backup_file = "C:/Backup_SQLproject/backup.sql"
    # Caminho completo para mysql
    mysql_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    # Comando para restaurar o backup
    restore_command = f'"{mysql_path}" -h {db_config["host"]} -u {db_config["user"]} -p{db_config["password"]} {db_config["database"]} < "{backup_file}"'
    # Executa a restauração no CMD
    process = subprocess.run(restore_command, shell=True,
                             capture_output=True, text=True)
    if process.returncode == 0:
        print(f"Backup restaurado com sucesso!")
    else:
        print(f"Erro ao restaurar backup: {process.stderr}")
