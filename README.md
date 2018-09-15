For English description look down.

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






[DESCRIPTION in English]

Parser analyzes access.log: collects source-ip, count of requests from each address.
Each address is checked for its blacklist reputation here https://ip.pentestit.ru.
Collected data is stored to CSV file, MySQL and PostgreSQl databases.
To facilitate reading data from databases two ancillary scripts were added:
	read_mysql.py
	read_postgresql.py

[FILES]

README.md		this file
REQUIREMENTS.txt	requirements list - necessary libraries
test.py			the parser itself
read_mysql.py		read MySQL data script (select *)
read_postgresql.py	read PostgreSQL data script (select *)
postgre.sql		SQL scheme for PostgreSQL DB (1 table)
my.sql			acheme for the same table in a MySQL DB
access.log		access.log example
out.csv			out file example

[USAGE]

Submit access log file and out file to script:
> python test.py access.log out.csv

if files are not submitted, you'll see this message:
> python test.py
usage: test.py [-h] in_file out_file
test.py: error: too few arguments

[ПРОВЕРКА]

Collected data will be written to three different datasets: Postgre and MySQL databases and in a CSV file.
You can get data from databases with help of ancillary scripts read_mysql.py, read_postgresql.py - run them without any args
