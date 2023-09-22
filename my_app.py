from flask import Flask, request, jsonify, render_template
from app.config.conn_db_settings import ConnectingDB
from app.views import Creattables, Foofordatabase


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Создаем подключение к базе данных (или создаем новую, если ее нет)
conn = ConnectingDB('machine_catalog').create_connection()
cursor = conn.cursor()
Creattables(cursor)


# Визуальное представление таблицы
@app.route('/')
def cars_table_in_db():
    cursor.execute('SELECT * FROM cars')
    rows = cursor.fetchall()
    return render_template('cars_db.html', rows=rows)


# Маршрут для вывода списка всех объектов
@app.route('/cars', methods=['GET'])
def list_cars():
    cars = Foofordatabase(cursor).get_all_cars()
    return jsonify(cars)


# Маршрут для добавления нового автомобиля
@app.route('/cars', methods=['POST'])
def create_car():
    error_messages = []  # Список для сохранения сообщений об ошибках
    datas = request.get_json()
    if type(datas) == dict:
        datas = [datas]
    for data in datas:
        print(data)
        number_plate = data.get('number_plate')
        car_make = data.get('car_make')
        color = data.get('color')
        year = data.get('year')
        engine_power = data.get('engine_power')
        transmission = data.get('transmission')
        fuel_type = data.get('fuel_type')
        car_mileage = data.get('car_mileage')
        car_price = data.get('car_price')

        if not number_plate or not car_make or not color or not year or not engine_power \
                or not transmission or not fuel_type or not car_mileage or not car_price:
            error_messages.append('Не все обязательные параметры указаны')
            continue
            # return jsonify({'message': 'Не все обязательные параметры указаны'}), 400

        # Проверяем, существует ли автомобиль с таким номером
        cursor.execute('SELECT id FROM cars WHERE number_plate = %s', (number_plate,))
        existing_car = cursor.fetchone()
        if existing_car:
            error_messages.append(f'Автомобиль с  номером {number_plate} уже существует')
            # return jsonify({'message': 'Автомобиль с таким номером уже существует'}), 409
            continue
        Foofordatabase(cursor).add_car(number_plate, car_make, color, year, engine_power, transmission,
                                       fuel_type, car_mileage, car_price)

    # return jsonify({'message': 'Автомобиль успешно добавлен'}), 201

    if error_messages:
        return jsonify({'Ошибка': error_messages}), 400
    else:
        return jsonify({'message': 'Автомобили успешно добавлены'}), 201


# Маршрут для удаления автомобиля по идентификатору
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    cursor.execute('SELECT id FROM cars WHERE id = %s', (car_id,))
    existing_car = cursor.fetchone()
    if not existing_car:
        return jsonify({'message': 'Автомобиль не найден'}), 404

    cursor.execute('DELETE FROM cars WHERE id = %s', (car_id,))
    return jsonify({'message': 'Автомобиль успешно удален'}), 200


# Маршрут для получения статистики
@app.route('/stats', methods=['GET'])
def get_stats():
    cursor.execute('SELECT COUNT(*) FROM cars')
    total_records = cursor.fetchone()[0]
    cursor.execute(
        'SELECT car_make, number_plate, MIN(year) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year ASC LIMIT 1')
    min_year = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MAX(year) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year DESC LIMIT 1')
    max_year = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MAX(car_mileage) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year DESC LIMIT 1')
    max_car_mileage = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MIN(car_mileage) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year ASC LIMIT 1')
    min_car_mileage = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MAX(car_price) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year DESC LIMIT 1')
    max_car_price = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MIN(car_price) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year ASC LIMIT 1')
    min_car_price = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MAX(date_add) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year DESC LIMIT 1')
    max_date_add = cursor.fetchone()

    cursor.execute(
        'SELECT car_make, number_plate, MIN(date_add) as year FROM cars GROUP BY car_make, number_plate '
        'ORDER BY year ASC LIMIT 1')
    min_date_add = cursor.fetchone()

    return jsonify({'total_count': total_records, 'min_year': min_year, 'max_year': max_year,
                    'max_car_mileage': max_car_mileage, 'min_car_mileage': min_car_mileage,
                    'max_car_price': max_car_price, 'min_car_price': min_car_price,
                    'max_date_add': max_date_add, 'min_date_add': min_date_add})


if __name__ == '__main__':
    app.run(debug=True)
