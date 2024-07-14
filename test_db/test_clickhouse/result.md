### Результаты тестирования БД Clickhouse

##### Время вставки записей в секундах:

____________________________________________________________________________
- **1000 записей (batch=500)**: 0.04088425636291504 секунд
- Среднее время вставки одной записи: 4.294323921203613e-05

- **100 000 записей (batch=500)**: 4.038236141204834 секунд
- Среднее время вставки одной записи: 4.038236141204834e-05 

- **1 000 000 записей (batch=500)**: 39.94157147407532 секунд
- Среднее время вставки одной записи:  3.994157147407532e-05 

- **10 000 000 записей (batch=500)**: 441.04130387306213 секунд
- Среднее время вставки одной записи: 4.4104130387306214e-05 секунд

------------------------------------------------------

- **1000 записей (batch=1000)**: 0.04452919960021973 секунд
- Среднее время вставки одной записи: 4.452919960021973e-05 секунд

- **100 000 записей (batch=100000)**: 4.266417980194092 секунд
- Среднее время вставки одной записи:  4.266417980194092e-05 секунд

- **1 000 000 записей (batch=100000)**: 40.99327778816223 секунд
- Среднее время вставки одной записи: 4.099327778816223e-05 секунд

- **10 000 000 записей (batch=100000)**: 425.2553403377533 секунд
- Среднее время вставки одной записи: 4.252553403377533e-05 секунд
____________________________________________________________________________

##### Считывние данных из таблицы и вывод их в стандартный поток вывода:

____________________________________________________________________________
- **100 000 записей**: 0.00534820556640625 секунд
- Среднее время получения одной записи: 5.34820556640625e-10
- **10 000 000 записей**:  0.005691051483154297 секунд
- Среднее время получения одной записи: 5.691051483154296e-10 секунд
___________________________________________________________________________

##### Обновление данных:

____________________________________________________________________________
- **100 000 записей**: 0.06716775894165039 секунд
- Среднее время обновления одной записи: 6.716775894165039e-07  секунд

- **10 000 000 записей**: 0.11500144004821777  секунд
- Среднее время обновления одной записи: 1.1500144004821778e-08 секунд
____________________________________________________________________________