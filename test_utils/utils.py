import time

def time_it(func):
    """Декоратор, измеряющий время выполнения функции"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time)
        speed_time = (execution_time / TOTAL)
        print(f"Скорость обработки {TOTAL} записей: {execution_time} секунд")
        print(f"Средняя скорость обработки одной записи из {TOTAL} записей: {speed_time} секунд")
        return result

    return wrapper


@time_it
def transform_data(event_generator, insert_events):
    """Преобразование данных и вставка в БД"""

    for batch in event_generator:
        values = [
            (event['type'],
             event['timestamp'],
             event['user_id'],
             event['fingerprint'],
             event['element'],
             event['url'])
            for event in batch
        ]

        insert_events(values)

