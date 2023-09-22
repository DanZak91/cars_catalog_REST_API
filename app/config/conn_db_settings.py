# Настройки подключения

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import OperationalError


class ConnectingDB:
    def __init__(self, name_db: str, user='postgres', password='123', host='localhost', port=5432):
        self.name_db = name_db
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def starter(self):
        """Подключение и настройка к имеющейся БД"""

        connection = psycopg2.connect(
            database=self.name_db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        print(f"Успешное подключение к БД PostgreSQL - {self.name_db}: {connection}")
        connection.autocommit = True
        return connection

    def create_new_db(self):
        """Создание новой БД в PostgreSQL"""

        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        sql_create_database = cursor.execute(f'create database {self.name_db}')
        print('Создана новая БД: ', self.name_db)
        conn.autocommit = True
        return self.starter()

    def create_connection(self):
        """Подключение к существующей или создание новой БД в случае отсутствия"""

        try:
            return self.starter()
        except OperationalError:
            return self.create_new_db()
