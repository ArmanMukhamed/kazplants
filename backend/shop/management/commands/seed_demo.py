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
            ("Фикус Бенджамина", "fikus-bendzhamina", "KP-001", "Kazplants", "D20", "Комнатные растения", "Неприхотливое комнатное растение для дома.", "in_stock", 95, 25, "Нидерланды", "easy", "Рассеянный свет", "1-2 раза в неделю", Decimal("8500.00"), True, True),
            ("Монстера Деликатесная", "monstera-delikatesnaya", "KP-002", "Kazplants", "D24", "Комнатные растения", "Эффектное растение с крупными листьями.", "in_stock", 120, 28, "Колумбия", "medium", "Яркий рассеянный", "2 раза в неделю", Decimal("12500.00"), True, True),
            ("Сансевиерия", "sansevieriya", "KP-003", "Kazplants", "D16", "Комнатные растения", "Подходит для офисов и квартир.", "low_stock", 65, 18, "Кения", "easy", "Полутень", "1 раз в 7-10 дней", Decimal("6400.00"), True, False),
            ("Замиокулькас", "zamiokulkas", "KP-004", "Kazplants", "D18", "Комнатные растения", "Стильное растение для современного интерьера.", "preorder", 70, 20, "Танзания", "easy", "Полутень", "1 раз в неделю", Decimal("9800.00"), False, True),
            ("Спатифиллум", "spatifillum", "KP-005", "Kazplants", "D15", "Комнатные растения", "Цветущее растение для дома.", "in_stock", 55, 16, "Эквадор", "medium", "Рассеянный", "2 раза в неделю", Decimal("7600.00"), False, False),
            ("Лимонное дерево", "limonnoe-derevo", "KP-006", "Kazplants", "D28", "Деревья и саженцы", "Саженец лимона для домашнего выращивания.", "in_stock", 110, 30, "Турция", "medium", "Яркий свет", "2-3 раза в неделю", Decimal("14900.00"), True, True),
            ("Яблоня Апорт", "yablonya-aport", "KP-007", "Kazplants", "D30", "Деревья и саженцы", "Саженец яблони для климата Казахстана.", "in_stock", 130, 35, "Казахстан", "easy", "Солнце", "2 раза в неделю", Decimal("9900.00"), True, False),
            ("Туя Смарагд", "tuya-smaragd", "KP-008", "Kazplants", "D22", "Деревья и саженцы", "Декоративный хвойный саженец.", "low_stock", 85, 22, "Польша", "easy", "Солнце/полутень", "1-2 раза в неделю", Decimal("11500.00"), True, False),
            ("Гортензия метельчатая", "gortenziya-metelchataya", "KP-009", "Kazplants", "D20", "Деревья и саженцы", "Пышные цветы для сада.", "preorder", 75, 24, "Франция", "medium", "Солнце", "2 раза в неделю", Decimal("13200.00"), False, True),
            ("Можжевельник", "mozhzhevelnik", "KP-010", "Kazplants", "D24", "Деревья и саженцы", "Вечнозеленый акцент для участка.", "in_stock", 90, 26, "Германия", "easy", "Солнце", "1-2 раза в неделю", Decimal("10700.00"), False, False),
            ("Роза красная", "roza-krasnaya", "KP-011", "BloomLine", "D12", "Цветы", "Классический цветок для подарка.", "in_stock", 45, 10, "Кения", "medium", "Яркий свет", "Ежедневно", Decimal("4500.00"), True, True),
            ("Пион розовый", "pion-rozovyy", "KP-012", "BloomLine", "D14", "Цветы", "Пышные бутоны и аромат.", "in_stock", 50, 12, "Нидерланды", "medium", "Солнце", "Через день", Decimal("5200.00"), True, True),
            ("Хризантема белая", "hrizantema-belaya", "KP-013", "BloomLine", "D12", "Цветы", "Долго сохраняет свежесть.", "low_stock", 40, 11, "Эквадор", "easy", "Рассеянный", "Ежедневно", Decimal("3900.00"), False, False),
            ("Тюльпан микс", "tyulpan-miks", "KP-014", "BloomLine", "D10", "Цветы", "Яркий весенний микс.", "in_stock", 35, 9, "Казахстан", "easy", "Яркий свет", "Ежедневно", Decimal("3100.00"), False, True),
            ("Лилия белая", "liliya-belaya", "KP-015", "BloomLine", "D16", "Цветы", "Изысканный букетный цветок.", "preorder", 60, 14, "Израиль", "medium", "Солнце", "Ежедневно", Decimal("6100.00"), False, False),
            ("Кашпо бетонное", "kashpo-betonnoe", "KP-016", "HomePot", "D24", "Кашпо и аксессуары", "Минималистичное кашпо серого цвета.", "in_stock", 28, 24, "Казахстан", "easy", "-", "-", Decimal("5800.00"), False, True),
            ("Кашпо керамическое", "kashpo-keramicheskoe", "KP-017", "HomePot", "D21", "Кашпо и аксессуары", "Глянцевое кашпо для интерьера.", "in_stock", 25, 21, "Китай", "easy", "-", "-", Decimal("4600.00"), False, False),
            ("Подставка для растений", "podstavka-dlya-rasteniy", "KP-018", "HomePot", "D35", "Кашпо и аксессуары", "Металлическая подставка на 3 уровня.", "in_stock", 75, 35, "Казахстан", "easy", "-", "-", Decimal("8900.00"), False, True),
            ("Опрыскиватель", "opryskivatel", "KP-019", "GardenCare", "D08", "Кашпо и аксессуары", "Ручной опрыскиватель для ухода.", "in_stock", 18, 8, "Китай", "easy", "-", "-", Decimal("2400.00"), False, False),
            ("Дренажный набор", "drenazhnyy-nabor", "KP-020", "GardenCare", "D18", "Кашпо и аксессуары", "Керамзит и подложка для пересадки.", "in_stock", 12, 18, "Казахстан", "easy", "-", "-", Decimal("1900.00"), False, False),
            ("Фитостена мини", "fitostena-mini", "KP-021", "Kazplants", "D60", "Готовые решения", "Готовая вертикальная композиция.", "preorder", 120, 60, "Казахстан", "medium", "Яркий рассеянный", "2 раза в неделю", Decimal("45900.00"), True, True),
            ("Офисный набор", "ofisnyy-nabor", "KP-022", "Kazplants", "D40", "Готовые решения", "Комплект растений для офиса.", "in_stock", 80, 40, "Казахстан", "easy", "Полутень", "1-2 раза в неделю", Decimal("28900.00"), True, False),
            ("Подарочный набор Грин", "podarochnyy-set-green", "KP-023", "Kazplants", "D25", "Готовые решения", "Набор из растения и кашпо.", "in_stock", 50, 25, "Казахстан", "easy", "Рассеянный", "1-2 раза в неделю", Decimal("17900.00"), False, True),
            ("Балконный набор", "balkonnyy-nabor", "KP-024", "Kazplants", "D30", "Готовые решения", "Набор цветущих растений для балкона.", "preorder", 65, 30, "Казахстан", "medium", "Солнце", "2-3 раза в неделю", Decimal("21400.00"), False, False),
            ("Набор для новичка", "nabor-dlya-novichka", "KP-025", "Kazplants", "D24", "Готовые решения", "Неприхотливые растения для старта.", "in_stock", 45, 24, "Казахстан", "easy", "Полутень", "1 раз в неделю", Decimal("13900.00"), True, False),
            ("Удобрение универсальное", "udobrenie-universalnoe", "KP-026", "GardenCare", "D06", "Уход и удобрения", "Подходит для большинства комнатных растений.", "in_stock", 18, 6, "Казахстан", "easy", "-", "По инструкции", Decimal("2100.00"), False, False),
            ("Грунт премиум", "grunt-premium", "KP-027", "GardenCare", "D08", "Уход и удобрения", "Питательный грунт для пересадки.", "in_stock", 20, 8, "Казахстан", "easy", "-", "-", Decimal("1700.00"), False, True),
            ("Стимулятор роста", "stimulyator-rosta", "KP-028", "GardenCare", "D05", "Уход и удобрения", "Ускоряет укоренение и рост.", "low_stock", 14, 5, "Россия", "easy", "-", "По инструкции", Decimal("2600.00"), False, False),
            ("Набор для пересадки", "nabor-dlya-peresadki", "KP-029", "GardenCare", "D10", "Уход и удобрения", "Инструменты и расходники для пересадки.", "preorder", 22, 10, "Китай", "easy", "-", "-", Decimal("3900.00"), False, True),
            ("Защита от вредителей", "zashchita-ot-vrediteley", "KP-030", "GardenCare", "D05", "Уход и удобрения", "Безопасное средство для профилактики.", "in_stock", 16, 5, "Казахстан", "easy", "-", "По инструкции", Decimal("2800.00"), False, False),
        ]

        created_count = 0
        updated_count = 0

        for (
            title,
            slug,
            sku,
            brand,
            pot_size,
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
                "sku": sku,
                "brand": brand,
                "pot_size": pot_size,
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
                "characteristics": f"""Артикул: {sku}
Бренд: {brand}
Категория: {category_name}
Свет: {light_requirements}
Полив: {watering}""",
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
