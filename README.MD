# Тестовый скрипт для создания html страниц из результатов json CIS проверки

Скрипт-парсер json файла, полученного в результате аудита системы по технологии
[[https://github.com/ansible-lockdown/RHEL8-CIS-Audit]]

# Установка

```
python -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt
```

# Запуск

## Положите файлы ``.json`` в каталог reports

```
python ./cis/main.py
```

## Результат будт доступен в папке results
