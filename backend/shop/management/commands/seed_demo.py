from decimal import Decimal

from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Create demo categories and products for Kazplants MVP"

    def handle(self, *args, **options):
        categories_data = [
            ("Комнатные растения", "komnatnye-rasteniya"),
            ("Деревья и саженцы", "derevya-i-sazhency"),
            ("Цветы", "cvety"),
        ]

        categories = {}
        for name, slug in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )
            categories[name] = category
            action = "created" if created else "exists"
            self.stdout.write(self.style.SUCCESS(f"Category {action}: {name}"))

        demo_products = [
            ("Фикус Бенджамина", "fikus-bendzhamina", "Комнатные растения", "Неприхотливое комнатное растение для дома.", Decimal("8500.00")),
            ("Монстера Деликатесная", "monstera-delikatesnaya", "Комнатные растения", "Эффектное растение с крупными листьями.", Decimal("12500.00")),
            ("Сансевиерия", "sansevieriya", "Комнатные растения", "Подходит для офисов и квартир, легко ухаживать.", Decimal("6400.00")),
            ("Лимонное дерево", "limonnoe-derevo", "Деревья и саженцы", "Саженец лимона для домашнего и тепличного выращивания.", Decimal("14900.00")),
            ("Яблоня Апорт", "yablonya-aport", "Деревья и саженцы", "Саженец яблони, адаптированный к климату Казахстана.", Decimal("9900.00")),
            ("Туя Смарагд", "tuya-smaragd", "Деревья и саженцы", "Декоративный хвойный саженец для участка.", Decimal("11500.00")),
            ("Роза красная", "roza-krasnaya", "Цветы", "Классический цветок для подарка и оформления.", Decimal("4500.00")),
            ("Пион розовый", "pion-rozovyy", "Цветы", "Пышные бутоны и приятный аромат.", Decimal("5200.00")),
            ("Хризантема белая", "hrizantema-belaya", "Цветы", "Долго сохраняет свежесть после срезки.", Decimal("3900.00")),
            ("Тюльпан микс", "tyulpan-miks", "Цветы", "Яркий весенний микс тюльпанов.", Decimal("3100.00")),
        ]

        created_count = 0
        for title, base_slug, category_name, description, price in demo_products:
            category = categories[category_name]
            slug = base_slug
            idx = 1
            while Product.objects.filter(slug=slug).exclude(title=title).exists():
                idx += 1
                slug = f"{base_slug}-{idx}"

            product, created = Product.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slug,
                    "category": category,
                    "description": description,
                    "price": price,
                    "stock_status": Product.StockStatus.IN_STOCK,
                    "characteristics": "Размер: средний\nУход: регулярный полив",
                    "is_active": True,
                    "meta_title": f"{title} | Kazplants",
                    "meta_description": description[:160],
                },
            )
            if not created:
                changed = False
                if product.category_id != category.id:
                    product.category = category
                    changed = True
                if product.price != price:
                    product.price = price
                    changed = True
                if not product.is_active:
                    product.is_active = True
                    changed = True
                if changed:
                    product.save(update_fields=["category", "price", "is_active"])
                self.stdout.write(f"Product exists: {title}")
                continue

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Product created: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created products: {created_count}"))
