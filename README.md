[ОПИСАНИЕ]
Парсер анализирует access.log: собирает source-ip, количество запросов с адреса.
Далее проверяется репутация каждого найденного адреса на сервисе https://ip.pentestit.ru.
Собранная информация сохраняется в CSV-файл, в базы MySQL и PostgreSQl.
Для упрощения проверки записи в базы написаны вспомогательные скрипты:
	read_mysql.py
	read_postgresql.py

[Краткое описание файлов]
README.txt		этот файл
REQUIREMENTS.txt	перечень зависимостей - необходимых компонентов
test.py			основной скрипт-парсер
read_mysql.py		скрипт для проверки данных в базе MySQL (select *)
read_postgresql.py	скрипт для проверки данных в базе PostgreSQL (select *)
postgre.sql		схема таблицы БД PostgreSQL
my.sql			схема таблицы БД mysql
access.log		образец лога для анализа

[ЗАПУСК]
для запуска необходимо указать файл анализируемого лога и выходной файл CSV:
> python test.py access.log out.csv

если файлы не указаны, скрипт сообщит о необходимости указания данных параметров:
> python test.py
usage: test.py [-h] in_file out_file
test.py: error: too few arguments

[ПРОВЕРКА]
Данные анализа должны быть записаны в три разных хранилища: в базы Postgre и MySQL, и в файл CSV
Данные из баз легко запросить скриптами read_mysql.py, read_postgresql.py - запускаются без параметров
