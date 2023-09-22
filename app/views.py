import datetime


class Creattables:
    """Создаем таблицу для хранения информации о автомобилях"""

    def __init__(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                number_plate CHARACTER VARYING(15) NOT NULL,
                car_make TEXT NOT NULL,
                color TEXT NOT NULL,
                year INTEGER NOT NULL,
                engine_power DOUBLE PRECISION NOT NULL,
                transmission TEXT NOT NULL,
                fuel_type TEXT NOT NULL,
                car_mileage INTEGER NOT NULL,
                car_price INTEGER NOT NULL,
                date_add TIMESTAMP NOT NULL 
            )
        ''')


class Foofordatabase:
    """для работы с таблицей БД"""

    def __init__(self, cursor, *args):
        self.cursor = cursor

    # Функция для добавления нового автомобиля
    def add_car(self, number_plate, car_make, color, year, engine_power, transmission, fuel_type, car_mileage,
                car_price):
        current_date = datetime.datetime.now()
        self.cursor.execute('INSERT INTO cars (number_plate, car_make, color, year, engine_power, transmission, '
                            'fuel_type, car_mileage, car_price, date_add) '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (number_plate, car_make, color, year, engine_power, transmission, fuel_type, car_mileage,
                             car_price, current_date))

    # Функция для получения списка всех автомобилей
    def get_all_cars(self):
        self.cursor.execute('SELECT * FROM cars')
        cars = [{'id': row[0], 'number_plate': row[1], 'car_make': row[2], 'color': row[3], 'year': row[4],
                 'engine_power': row[5], 'transmission': row[6], 'fuel_type': row[7], 'car_mileage': row[8],
                 'car_price': row[9], 'date_add': row[10]} for row in self.cursor.fetchall()]
        return cars
