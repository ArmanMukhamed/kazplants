# Kazplants MVP

Kazplants — гибридный MVP интернет-магазина растений по Казахстану на Django.

## Стек
- Django
- Django Admin
- Django Templates
- SQLite
- Bootstrap 5 + custom CSS

## Язык MVP
- MVP работает только на русском языке.

## Что реализовано
- Маркетплейс-стиль витрины в природной палитре
- Sticky header: меню, поиск, WhatsApp кнопка, mobile burger
- Главная с hero и секциями
- Категории карточками
- Каталог с фильтрами и сортировкой
- Карточка товара с параметрами растения и похожими товарами
- Заказ только через WhatsApp с автосообщением
- Улучшенная Django Admin
- `sitemap.xml`

## Модели
- `Category`
- `Product`
- `ProductImage`

## Как запустить проект локально

1. Перейти в backend:
```bash
cd backend
```

2. Активировать venv:
```bash
source venv/bin/activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Применить миграции:
```bash
python manage.py migrate
```

5. Заполнить демо-данные:
```bash
python manage.py seed_demo
```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить сервер:
```bash
python manage.py runserver
```

## Основные URL
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/catalog/`
- `http://127.0.0.1:8000/categories/`
- `http://127.0.0.1:8000/about/`
- `http://127.0.0.1:8000/contacts/`
- `http://127.0.0.1:8000/admin/`
- `http://127.0.0.1:8000/sitemap.xml`

## Документация
- [PROJECT_PLAN.md](docs/PROJECT_PLAN.md)
- [LAUNCH_GUIDE.md](docs/LAUNCH_GUIDE.md)
