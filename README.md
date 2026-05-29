# Kazplants MVP

MVP интернет-магазина растений по Казахстану на Django.

## Стек
- Django 5
- Django Admin
- Django Templates
- SQLite
- Bootstrap 5

## Реализовано в MVP
- Главная страница
- Каталог товаров
- Поиск по названию товара
- Категории и страница категории
- Карточка товара с галереей
- Кнопка покупки через WhatsApp с автосообщением
- О компании, Контакты, 404
- SEO-база: slug, meta title, meta description, clean URLs
- Sitemap readiness: `/sitemap.xml`
- i18n интерфейса: RU / KZ / EN
- Админка для управления категориями, товарами и изображениями

## Структура

```text
kazplants/
├── backend/
├── docs/
├── static/
├── media/
├── templates/
├── README.md
└── .gitignore
```

## Запуск локально

1. Перейти в backend:
```bash
cd backend
```

2. Активировать виртуальное окружение (если нужно):
```bash
source venv/bin/activate
```

3. Применить миграции:
```bash
python3 manage.py migrate
```

4. Создать администратора:
```bash
python3 manage.py createsuperuser
```

5. Запустить сервер:
```bash
python3 manage.py runserver
```

6. Открыть:
- сайт: `http://127.0.0.1:8000/ru/`
- админка: `http://127.0.0.1:8000/admin/`

## Важные настройки
В `backend/config/settings.py`:
- `WHATSAPP_PHONE` — номер для кнопки заказа
- `LANGUAGES` — поддерживаемые языки интерфейса
- `MEDIA_ROOT`, `MEDIA_URL` — хранение и выдача изображений

## Модели
- `Category`
- `Product`
- `ProductImage`

Описание архитектуры и roadmap: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)
