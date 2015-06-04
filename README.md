# ii-ssh

 Здесь находится реализация sftp-транспорта для сети ii. Эти простейшие скрипты - просто "proof-of-concept", хотя и работают.

 У клиента должны быть: bash, sshfs, [ii-db-utils](https://github.com/vit1-irk/ii-db-utils) (для offline-fetch.py)
 На сервере нужен ssh со включенным sftp.

###### Установка на сервере
```bash
# iissh-setup.sh
# iissh-point.sh <имя поинта>
[тут спросят пароль для него]
```

 Затем добавляете скрипт `toss.py` в cron к пользователю iissh.

###### Использование на клиенте
 Отредактируйте файл `sshfetch.sh`, укажите имя пользователя, параметры подключения, путь к `offline-fetch.py` и подписки на эхоконференции.

 Потом просто набираете `sshfetch.sh fetch` для получения сообщений и `sshfetch.sh send` для отправки.
 Формат файлов .toss - plaintext [msgline](http://ii-net.tk/ii-doc/?p=2#pointmsg).
