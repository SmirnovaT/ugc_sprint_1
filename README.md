#### ONLINE CINEMA SERVICE

____________________________________________________________________________
[Ссылка на репозиторий](https://github.com/SmirnovaT/ugc_sprint_1)
____________________________________________________________________________

Запуск проекта с docker compose

Необходимо заполнить .env по шаблону .env_example

```
docker-compose up --build
or
docker-compose up --build -d
```

____________________________________________________________________________
Тестирование приложения локально:

```
1. cd tests/

2. python3 -m pytest
or 
   pytest -k <test_name> (python3 -m pytest -k <test_name>)
```
____________________________________________________________________________
[Результаты тестирования Vertica](test_vertica/result.md)
____________________________________________________________________________
Architectural diagram AS IS
____________________________________________________________________________
![arch as is](assets/arch_as_is.png)


____________________________________________________________________________
Architectural diagram TO BE
____________________________________________________________________________
![arch to_be](assets/arch_to_be.jpg)

[Результаты тестирования Vertica](test_db/test_vertica/result.md)

[Результаты тестирования ClickHouse](test_db/test_clickhouse/result.md)