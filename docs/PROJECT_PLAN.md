# PROJECT PLAN: Kazplants Russian-only MVP

## 1. Цель
Создать красивый и быстрый MVP интернет-магазина растений, где:
- гость смотрит каталог и покупает через WhatsApp;
- администратор управляет данными через Django Admin.

## 2. Архитектура
- Backend: Django (монолит), Django Admin, Django Templates
- Database: SQLite
- Frontend: Bootstrap + кастомный CSS (mobile-first)
- Без React, Next.js, Docker, микросервисов

## 3. Язык
- MVP работает только на русском языке.

## 4. Основной сценарий
1. Гость заходит на главную.
2. Переходит в каталог.
3. Фильтрует по параметрам растения.
4. Открывает карточку товара.
5. Нажимает «Купить через WhatsApp».

## 5. Функциональные модули MVP
- Главная с hero + секции популярных/новых товаров
- Категории карточками
- Каталог с фильтрами и сортировками
- Карточка товара с параметрами и похожими товарами
- WhatsApp-only checkout
- Улучшенная админка

## 6. Данные и модели
### Category
- name, slug, image, created_at

### Product
- title, slug, category, description, price, image, stock_status
- height, diameter, origin_country, care_level, light_requirements, watering
- characteristics, is_active, is_popular, is_new
- meta_title, meta_description, created_at

### ProductImage
- product, image

## 7. Фильтры каталога
- категория
- цена (от/до)
- наличие
- высота (от/до)
- диаметр (от/до)
- сортировка: default, price asc, price desc, title A-Z
- пагинация и сброс фильтров

## 8. WhatsApp формат заказа
Сообщение формируется автоматически:
- Здравствуйте!
- Хочу заказать товар: [Название]
- Цена: [Цена]
- Высота: [Высота]
- Диаметр: [Диаметр]
- Ссылка: [URL товара]

Номер хранится в `settings.py` (`WHATSAPP_PHONE`).

## 9. Контент и demo seed
`seed_demo` создает:
- 6 категорий;
- 30+ товаров;
- параметры высоты/диаметра/ухода;
- флаги `is_popular`, `is_new`.

## 10. Критерии готовности
- Админка позволяет вести каталог без кода
- Мобильная версия корректна
- Каталог фильтруется и сортируется
- Карточка товара содержит ключевые параметры
- WhatsApp заказ работает стабильно
