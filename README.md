# loader-files
loader files

`sftp` сервис сущетсвует в качестве примера , в нем находится два файла по пути `./sftp_server/files`

сервис `migration` эмулирует какое-то приложение, которое управляет миграциями и умеет создавать записи в бд, на этапе сборки контейнеров будут добавлены две записи в БД в таблицу `server`, для примера

запуск задач по загрузке файлов произойдет после того, как окружение и информация по серверам будет подготовлена

запуск сервисов `docker-compose up --build -d`

postgres локально будет доступен на `postgres:potgres@localhost:5433/upload`



task1 - это задача `check_servers`

task2 - это задача `download_new_files`

task3 - это задача `process_file`

task4 - это задача `notify_file_uploaded`

<img width="1412" height="950" alt="image" src="https://github.com/user-attachments/assets/8864bfa8-baf7-48df-9f12-7b5e5faa379d" />

