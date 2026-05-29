# LAUNCH GUIDE: Kazplants Russian-only MVP

Шаг 1:
```bash
cd backend
```

Шаг 2:
```bash
source venv/bin/activate
```

Шаг 3:
```bash
pip install -r requirements.txt
```

Шаг 4:
```bash
python manage.py migrate
```

Шаг 5:
```bash
python manage.py seed_demo
```

Шаг 6:
```bash
python manage.py createsuperuser
```

Шаг 7:
```bash
python manage.py runserver
```

Шаг 8: открыть
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/catalog/
- http://127.0.0.1:8000/categories/
- http://127.0.0.1:8000/admin/

## Проверка WhatsApp-заказа
1. Откройте любой товар.
2. Нажмите «Купить через WhatsApp».
3. Убедитесь, что сообщение содержит:
- название товара
- цену
- высоту
- диаметр
- ссылку на товар
