from django.core.management.base import BaseCommand
from User.models import Wealthlevel

class Command(BaseCommand):
    help = 'Creates initial Wealthlevel data'

    def handle(self, *args, **kwargs):
        levels_data = [
            # BRASS LEVELS (1-19)
            {"level": 1, "min_coins": 0, "max_coins": 1999, "badge": "brass"},
            {"level": 2, "min_coins": 2000, "max_coins": 4999, "badge": "brass"},
            {"level": 3, "min_coins": 5000, "max_coins": 6999, "badge": "brass"},
            {"level": 4, "min_coins": 7000, "max_coins": 14999, "badge": "brass"},
            {"level": 5, "min_coins": 15000, "max_coins": 24999, "badge": "brass"},
            {"level": 6, "min_coins": 25000, "max_coins": 34999, "badge": "brass"},
            {"level": 7, "min_coins": 35000, "max_coins": 49999, "badge": "brass"},
            {"level": 8, "min_coins": 50000, "max_coins": 69999, "badge": "brass"},
            {"level": 9, "min_coins": 70000, "max_coins": 149999, "badge": "brass"},
            {"level": 10, "min_coins": 150000, "max_coins": 199999, "badge": "brass"},
            {"level": 11, "min_coins": 200000, "max_coins": 249999, "badge": "brass"},
            {"level": 12, "min_coins": 250000, "max_coins": 299999, "badge": "brass"},
            {"level": 13, "min_coins": 300000, "max_coins": 349999, "badge": "brass"},
            {"level": 14, "min_coins": 350000, "max_coins": 399999, "badge": "brass"},
            {"level": 15, "min_coins": 400000, "max_coins": 449999, "badge": "brass"},
            {"level": 16, "min_coins": 450000, "max_coins": 499999, "badge": "brass"},
            {"level": 17, "min_coins": 500000, "max_coins": 599999, "badge": "brass"},
            {"level": 18, "min_coins": 600000, "max_coins": 699999, "badge": "brass"},
            {"level": 19, "min_coins": 700000, "max_coins": 999999, "badge": "brass"},
            
            # SILVER LEVELS (20-40)
            {"level": 20, "min_coins": 1000000, "max_coins": 1999999, "badge": "silver"},
            {"level": 21, "min_coins": 2000000, "max_coins": 2999999, "badge": "silver"},
            {"level": 22, "min_coins": 3000000, "max_coins": 3999999, "badge": "silver"},
            {"level": 23, "min_coins": 4000000, "max_coins": 4999999, "badge": "silver"},
            {"level": 24, "min_coins": 5000000, "max_coins": 5999999, "badge": "silver"},
            {"level": 25, "min_coins": 6000000, "max_coins": 6999999, "badge": "silver"},
            {"level": 26, "min_coins": 7000000, "max_coins": 7999999, "badge": "silver"},
            {"level": 27, "min_coins": 8000000, "max_coins": 8999999, "badge": "silver"},
            {"level": 28, "min_coins": 9000000, "max_coins": 9999999, "badge": "silver"},
            {"level": 29, "min_coins": 10000000, "max_coins": 10999999, "badge": "silver"},
            {"level": 30, "min_coins": 11000000, "max_coins": 11999999, "badge": "silver"},
            {"level": 31, "min_coins": 12000000, "max_coins": 12999999, "badge": "silver"},
            {"level": 32, "min_coins": 13000000, "max_coins": 13999999, "badge": "silver"},
            {"level": 33, "min_coins": 14000000, "max_coins": 14999999, "badge": "silver"},
            {"level": 34, "min_coins": 15000000, "max_coins": 15999999, "badge": "silver"},
            {"level": 35, "min_coins": 16000000, "max_coins": 16999999, "badge": "silver"},
            {"level": 36, "min_coins": 17000000, "max_coins": 17999999, "badge": "silver"},
            {"level": 37, "min_coins": 18000000, "max_coins": 18999999, "badge": "silver"},
            {"level": 38, "min_coins": 19000000, "max_coins": 19999999, "badge": "silver"},
            {"level": 39, "min_coins": 20000000, "max_coins": 21999999, "badge": "silver"},
            {"level": 40, "min_coins": 22000000, "max_coins": 23999999, "badge": "silver"},

            # GOLD LEVELS (41-60)
            {"level": 41, "min_coins": 24000000, "max_coins": 25999999, "badge": "gold"},
            {"level": 42, "min_coins": 26000000, "max_coins": 27999999, "badge": "gold"},
            {"level": 43, "min_coins": 28000000, "max_coins": 29999999, "badge": "gold"},
            {"level": 44, "min_coins": 30000000, "max_coins": 32999999, "badge": "gold"},
            {"level": 45, "min_coins": 33000000, "max_coins": 35999999, "badge": "gold"},
            {"level": 46, "min_coins": 36000000, "max_coins": 38999999, "badge": "gold"},
            {"level": 47, "min_coins": 39000000, "max_coins": 41999999, "badge": "gold"},
            {"level": 48, "min_coins": 42000000, "max_coins": 44999999, "badge": "gold"},
            {"level": 49, "min_coins": 45000000, "max_coins": 47999999, "badge": "gold"},
            {"level": 50, "min_coins": 48000000, "max_coins": 54999999, "badge": "gold"},
            {"level": 51, "min_coins": 55000000, "max_coins": 59999999, "badge": "gold"},
            {"level": 52, "min_coins": 60000000, "max_coins": 64999999, "badge": "gold"},
            {"level": 53, "min_coins": 65000000, "max_coins": 69999999, "badge": "gold"},
            {"level": 54, "min_coins": 70000000, "max_coins": 74999999, "badge": "gold"},
            {"level": 55, "min_coins": 75000000, "max_coins": 79999999, "badge": "gold"},
            {"level": 56, "min_coins": 80000000, "max_coins": 84999999, "badge": "gold"},
            {"level": 57, "min_coins": 85000000, "max_coins": 89999999, "badge": "gold"},
            {"level": 58, "min_coins": 90000000, "max_coins": 94999999, "badge": "gold"},
            {"level": 59, "min_coins": 95000000, "max_coins": 99999999, "badge": "gold"},
            {"level": 60, "min_coins": 100000000, "max_coins": 109999999, "badge": "gold"},
            
            # DIAMOND LEVELS (61-100)
            {"level": 61, "min_coins": 110000000, "max_coins": 119999999, "badge": "diamond"},
            {"level": 62, "min_coins": 120000000, "max_coins": 129999999, "badge": "diamond"},
            {"level": 63, "min_coins": 130000000, "max_coins": 139999999, "badge": "diamond"},
            {"level": 64, "min_coins": 140000000, "max_coins": 149999999, "badge": "diamond"},
            {"level": 65, "min_coins": 150000000, "max_coins": 159999999, "badge": "diamond"},
            {"level": 66, "min_coins": 160000000, "max_coins": 169999999, "badge": "diamond"},
            {"level": 67, "min_coins": 170000000, "max_coins": 179999999, "badge": "diamond"},
            {"level": 68, "min_coins": 180000000, "max_coins": 189999999, "badge": "diamond"},
            {"level": 69, "min_coins": 190000000, "max_coins": 199999999, "badge": "diamond"},
            {"level": 70, "min_coins": 200000000, "max_coins": 209999999, "badge": "diamond"},
            {"level": 71, "min_coins": 210000000, "max_coins": 219999999, "badge": "diamond"},
            {"level": 72, "min_coins": 220000000, "max_coins": 229999999, "badge": "diamond"},
            {"level": 73, "min_coins": 230000000, "max_coins": 239999999, "badge": "diamond"},
            {"level": 74, "min_coins": 240000000, "max_coins": 249999999, "badge": "diamond"},
            {"level": 75, "min_coins": 250000000, "max_coins": 259999999, "badge": "diamond"},
            {"level": 76, "min_coins": 260000000, "max_coins": 269999999, "badge": "diamond"},
            {"level": 77, "min_coins": 270000000, "max_coins": 279999999, "badge": "diamond"},
            {"level": 78, "min_coins": 280000000, "max_coins": 289999999, "badge": "diamond"},
            {"level": 79, "min_coins": 290000000, "max_coins": 299999999, "badge": "diamond"},
            {"level": 80, "min_coins": 300000000, "max_coins": 349999999, "badge": "diamond"},
            {"level": 81, "min_coins": 350000000, "max_coins": 399999999, "badge": "diamond"},
            {"level": 82, "min_coins": 400000000, "max_coins": 449999999, "badge": "diamond"},
            {"level": 83, "min_coins": 450000000, "max_coins": 499999999, "badge": "diamond"},
            {"level": 84, "min_coins": 500000000, "max_coins": 549999999, "badge": "diamond"},
            {"level": 85, "min_coins": 550000000, "max_coins": 649999999, "badge": "diamond"},
            {"level": 86, "min_coins": 650000000, "max_coins": 699999999, "badge": "diamond"},
            {"level": 87, "min_coins": 700000000, "max_coins": 799999999, "badge": "diamond"},
            {"level": 88, "min_coins": 800000000, "max_coins": 899999999, "badge": "diamond"},
            {"level": 89, "min_coins": 900000000, "max_coins": 999999999, "badge": "diamond"},
            {"level": 90, "min_coins": 1000000000, "max_coins": 1099999999, "badge": "diamond"},
            {"level": 91, "min_coins": 1100000000, "max_coins": 1499999999, "badge": "diamond"},
            {"level": 92, "min_coins": 1500000000, "max_coins": 1999999999, "badge": "diamond"},
            {"level": 93, "min_coins": 2000000000, "max_coins": 2499999999, "badge": "diamond"},
            {"level": 94, "min_coins": 2500000000, "max_coins": 2999999999, "badge": "diamond"},
            {"level": 95, "min_coins": 3000000000, "max_coins": 3499999999, "badge": "diamond"},
            {"level": 96, "min_coins": 3500000000, "max_coins": 3999999999, "badge": "diamond"},
            {"level": 97, "min_coins": 4000000000, "max_coins": 4999999999, "badge": "diamond"},
            {"level": 98, "min_coins": 5000000000, "max_coins": 5999999999, "badge": "diamond"},
            {"level": 99, "min_coins": 6000000000, "max_coins": 99999999999, "badge": "diamond"},
            {"level": 100, "min_coins": 100000000000, "max_coins": 50000000000000, "badge": "diamond"}
        ]

        created_count = 0
        updated_count = 0
        
        for data in levels_data:
            obj, created = Wealthlevel.objects.update_or_create(
                level=data["level"], 
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created Level {data['level']} ({data['badge']})")
            else:
                updated_count += 1
                self.stdout.write(f"Updated Level {data['level']} ({data['badge']})")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(levels_data)} levels: '
                f'{created_count} created, {updated_count} updated'
            )
        )
        
        # Summary of level distribution
        self.stdout.write("\nLevel Distribution:")
        self.stdout.write(f"• Brass Levels: 1-19 (19 levels)")
        self.stdout.write(f"• Silver Levels: 20-40 (21 levels)")
        self.stdout.write(f"• Gold Levels: 41-60 (20 levels)")
        self.stdout.write(f"• Diamond Levels: 61-100 (40 levels)")
        self.stdout.write(f"Total: 100 levels")