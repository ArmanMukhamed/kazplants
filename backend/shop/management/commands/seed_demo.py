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
            ("Кашпо и аксессуары", "kashpo-i-aksessuary"),
            ("Готовые решения", "gotovye-resheniya"),
            ("Уход и удобрения", "uhod-i-udobreniya"),
        ]

        categories = {}
        for name, slug in categories_data:
            category, created = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            if category.name != name:
                category.name = name
                category.save(update_fields=["name"])
            categories[name] = category
            action = "created" if created else "exists"
            self.stdout.write(self.style.SUCCESS(f"Category {action}: {name}"))

        demo_products = [
            ("Фикус Бенджамина", "fikus-bendzhamina", "Комнатные растения", "Неприхотливое комнатное растение для дома.", "in_stock", 95, 25, "Нидерланды", "easy", "Рассеянный свет", "1-2 раза в неделю", Decimal("8500.00"), True, True),
            ("Монстера Деликатесная", "monstera-delikatesnaya", "Комнатные растения", "Эффектное растение с крупными листьями.", "in_stock", 120, 28, "Колумбия", "medium", "Яркий рассеянный", "2 раза в неделю", Decimal("12500.00"), True, True),
            ("Сансевиерия", "sansevieriya", "Комнатные растения", "Подходит для офисов и квартир.", "in_stock", 65, 18, "Кения", "easy", "Полутень", "1 раз в 7-10 дней", Decimal("6400.00"), True, False),
            ("Замиокулькас", "zamiokulkas", "Комнатные растения", "Стильное растение для современного интерьера.", "preorder", 70, 20, "Танзания", "easy", "Полутень", "1 раз в неделю", Decimal("9800.00"), False, True),
            ("Спатифиллум", "spatifillum", "Комнатные растения", "Цветущее растение для дома.", "in_stock", 55, 16, "Эквадор", "medium", "Рассеянный", "2 раза в неделю", Decimal("7600.00"), False, False),
            ("Лимонное дерево", "limonnoe-derevo", "Деревья и саженцы", "Саженец лимона для домашнего выращивания.", "in_stock", 110, 30, "Турция", "medium", "Яркий свет", "2-3 раза в неделю", Decimal("14900.00"), True, True),
            ("Яблоня Апорт", "yablonya-aport", "Деревья и саженцы", "Саженец яблони для климата Казахстана.", "in_stock", 130, 35, "Казахстан", "easy", "Солнце", "2 раза в неделю", Decimal("9900.00"), True, False),
            ("Туя Смарагд", "tuya-smaragd", "Деревья и саженцы", "Декоративный хвойный саженец.", "in_stock", 85, 22, "Польша", "easy", "Солнце/полутень", "1-2 раза в неделю", Decimal("11500.00"), True, False),
            ("Гортензия метельчатая", "gortenziya-metelchataya", "Деревья и саженцы", "Пышные цветы для сада.", "preorder", 75, 24, "Франция", "medium", "Солнце", "2 раза в неделю", Decimal("13200.00"), False, True),
            ("Можжевельник", "mozhzhevelnik", "Деревья и саженцы", "Вечнозеленый акцент для участка.", "in_stock", 90, 26, "Германия", "easy", "Солнце", "1-2 раза в неделю", Decimal("10700.00"), False, False),
            ("Роза красная", "roza-krasnaya", "Цветы", "Классический цветок для подарка.", "in_stock", 45, 10, "Кения", "medium", "Яркий свет", "Ежедневно", Decimal("4500.00"), True, True),
            ("Пион розовый", "pion-rozovyy", "Цветы", "Пышные бутоны и аромат.", "in_stock", 50, 12, "Нидерланды", "medium", "Солнце", "Через день", Decimal("5200.00"), True, True),
            ("Хризантема белая", "hrizantema-belaya", "Цветы", "Долго сохраняет свежесть.", "in_stock", 40, 11, "Эквадор", "easy", "Рассеянный", "Ежедневно", Decimal("3900.00"), False, False),
            ("Тюльпан микс", "tyulpan-miks", "Цветы", "Яркий весенний микс.", "in_stock", 35, 9, "Казахстан", "easy", "Яркий свет", "Ежедневно", Decimal("3100.00"), False, True),
            ("Лилия белая", "liliya-belaya", "Цветы", "Изысканный букетный цветок.", "preorder", 60, 14, "Израиль", "medium", "Солнце", "Ежедневно", Decimal("6100.00"), False, False),
            ("Кашпо бетонное", "kashpo-betonnoe", "Кашпо и аксессуары", "Минималистичное кашпо серого цвета.", "in_stock", 28, 24, "Казахстан", "easy", "-", "-", Decimal("5800.00"), False, True),
            ("Кашпо керамическое", "kashpo-keramicheskoe", "Кашпо и аксессуары", "Глянцевое кашпо для интерьера.", "in_stock", 25, 21, "Китай", "easy", "-", "-", Decimal("4600.00"), False, False),
            ("Подставка для растений", "podstavka-dlya-rasteniy", "Кашпо и аксессуары", "Металлическая подставка на 3 уровня.", "in_stock", 75, 35, "Казахстан", "easy", "-", "-", Decimal("8900.00"), False, True),
            ("Опрыскиватель", "opryskivatel", "Кашпо и аксессуары", "Ручной опрыскиватель для ухода.", "in_stock", 18, 8, "Китай", "easy", "-", "-", Decimal("2400.00"), False, False),
            ("Дренажный набор", "drenazhnyy-nabor", "Кашпо и аксессуары", "Керамзит и подложка для пересадки.", "in_stock", 12, 18, "Казахстан", "easy", "-", "-", Decimal("1900.00"), False, False),
            ("Фитостена мини", "fitostena-mini", "Готовые решения", "Готовая вертикальная композиция.", "preorder", 120, 60, "Казахстан", "medium", "Яркий рассеянный", "2 раза в неделю", Decimal("45900.00"), True, True),
            ("Офисный набор", "ofisnyy-nabor", "Готовые решения", "Комплект растений для офиса.", "in_stock", 80, 40, "Казахстан", "easy", "Полутень", "1-2 раза в неделю", Decimal("28900.00"), True, False),
            ("Подарочный набор Грин", "podarochnyy-set-green", "Готовые решения", "Набор из растения и кашпо.", "in_stock", 50, 25, "Казахстан", "easy", "Рассеянный", "1-2 раза в неделю", Decimal("17900.00"), False, True),
            ("Балконный набор", "balkonnyy-nabor", "Готовые решения", "Набор цветущих растений для балкона.", "preorder", 65, 30, "Казахстан", "medium", "Солнце", "2-3 раза в неделю", Decimal("21400.00"), False, False),
            ("Набор для новичка", "nabor-dlya-novichka", "Готовые решения", "Неприхотливые растения для старта.", "in_stock", 45, 24, "Казахстан", "easy", "Полутень", "1 раз в неделю", Decimal("13900.00"), True, False),
            ("Удобрение универсальное", "udobrenie-universalnoe", "Уход и удобрения", "Подходит для большинства комнатных растений.", "in_stock", 18, 6, "Казахстан", "easy", "-", "По инструкции", Decimal("2100.00"), False, False),
            ("Грунт премиум", "grunt-premium", "Уход и удобрения", "Питательный грунт для пересадки.", "in_stock", 20, 8, "Казахстан", "easy", "-", "-", Decimal("1700.00"), False, True),
            ("Стимулятор роста", "stimulyator-rosta", "Уход и удобрения", "Ускоряет укоренение и рост.", "in_stock", 14, 5, "Россия", "easy", "-", "По инструкции", Decimal("2600.00"), False, False),
            ("Набор для пересадки", "nabor-dlya-peresadki", "Уход и удобрения", "Инструменты и расходники для пересадки.", "preorder", 22, 10, "Китай", "easy", "-", "-", Decimal("3900.00"), False, True),
            ("Защита от вредителей", "zashchita-ot-vrediteley", "Уход и удобрения", "Безопасное средство для профилактики.", "in_stock", 16, 5, "Казахстан", "easy", "-", "По инструкции", Decimal("2800.00"), False, False),
        ]

        created_count = 0
        updated_count = 0

        for (
            title,
            slug,
            category_name,
            description,
            stock_status,
            height,
            diameter,
            origin_country,
            care_level,
            light_requirements,
            watering,
            price,
            is_popular,
            is_new,
        ) in demo_products:
            category = categories[category_name]
            defaults = {
                "title": title,
                "category": category,
                "description": description,
                "price": price,
                "stock_status": stock_status,
                "height": Decimal(str(height)),
                "diameter": Decimal(str(diameter)),
                "origin_country": origin_country,
                "care_level": care_level,
                "light_requirements": light_requirements,
                "watering": watering,
                "characteristics": (
                    f"""Категория: {category_name}
Свет: {light_requirements}
Полив: {watering}"""
                ),
                "is_active": True,
                "is_popular": is_popular,
                "is_new": is_new,
                "meta_title": f"{title} | Kazplants",
                "meta_description": description[:160],
            }

            product, created = Product.objects.update_or_create(slug=slug, defaults=defaults)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Product created: {title}"))
            else:
                updated_count += 1
                self.stdout.write(f"Product updated: {title}")

        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created_count}, Updated: {updated_count}"))
