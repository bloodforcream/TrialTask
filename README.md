## Инструкция по установке
```
pip install -r requirements.txt
python manage.py migrate
```

Также необходим суперюзер, если хотим работать с админкой (`localhost:8000/admin`): `python manage.py createsuperuser`

И наконец, сам запуск сервиса: `python manage.py runserver 127.0.0.1:8000`

## Инструкция по работе с API

### POST /api/auth/
Получение токена аутентификации
+ Request
        
        POST /api/auth/

+ Body

        {
            "username": "admin",
            "password": "12345678",
        }
 
        
+ Response 200

        {
            "token": "768772e7829f7cef0551eea171d1d16c37b8cef2"
        }
        
        
        
Во всех последующих запросах, юзер должен быть авторизован (токен аутентификации присутствует в хедерах запроса)

Пример хедера: `Authorization: Token 768772e7829f7cef0551eea171d1d16c37b8cef2`


### GET /api/test/
Получение информации о приложении.  Юзер должен быть связан с приложением 
+ Request
        
        GET /api/test/?key=5bcb741f-ee19-49e3-9164-8ee038b62dfa
 
        
+ Response 200

        {
            "name": ""
        }


### POST /api/test/create/
Создание приложения
+ Request
        
        POST /api/test/create/

+ Body

        {
            "name": "app1",
        }
 
        
+ Response 200

        {
            "name": "app1",
            "key": "01bd15dc-395b-4bc8-be19-868b7eda5b7f"
        }

### POST /api/test/update/
Обновление приложения. Юзер должен быть связан с приложением 
+ Request
        
        POST /api/test/update/

+ Body

        {
            "name": "app2",
            "key": "01bd15dc-395b-4bc8-be19-868b7eda5b7f",
        }
 
        
+ Response 200

        {
            "name": "app2",
            "key": "01bd15dc-395b-4bc8-be19-868b7eda5b7f"
        }
        
        
### POST /api/test/delete/
Удаление приложения. Юзер должен быть связан с приложением 
+ Request
        
        POST /api/test/delete/

+ Body

        {
            "key": "01bd15dc-395b-4bc8-be19-868b7eda5b7f",
        }
 
        
+ Response 200

        {
            "status": "ok"
        }
        
## Кастомные команды django
Для генерации нового ключа для существующего приложения используем: `python manage.py change_key {old_key}`