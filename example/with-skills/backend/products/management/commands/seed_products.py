from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Create sample products for local development."

    def handle(self, *args, **options) -> None:
        products = [
            {
                "name": "Structured Wool Overshirt",
                "category": "men",
                "description": "Warm wool-blend overshirt with clean lines for weekday layering.",
                "price": Decimal("89.00"),
                "image_url": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Relaxed Linen Shirt",
                "category": "men",
                "description": "Breathable linen shirt cut for an easy weekend fit.",
                "price": Decimal("58.00"),
                "image_url": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Tailored Wide-Leg Trousers",
                "category": "women",
                "description": "Fluid trousers with a high waist and polished drape.",
                "price": Decimal("76.00"),
                "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Ribbed Knit Cardigan",
                "category": "women",
                "description": "Soft ribbed cardigan designed for cool mornings and late dinners.",
                "price": Decimal("64.00"),
                "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Kids Colorblock Hoodie",
                "category": "kids",
                "description": "Durable cotton hoodie with playful colorblocking and roomy pockets.",
                "price": Decimal("34.00"),
                "image_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Kids Everyday Joggers",
                "category": "kids",
                "description": "Soft joggers built for school days, playgrounds, and couch time.",
                "price": Decimal("29.00"),
                "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Canvas Crossbody Bag",
                "category": "accessories",
                "description": "Compact daily bag with an adjustable strap and secure inner pocket.",
                "price": Decimal("42.00"),
                "image_url": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Merino Beanie",
                "category": "accessories",
                "description": "Fine merino beanie with a clean folded edge and soft hand feel.",
                "price": Decimal("24.00"),
                "image_url": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?auto=format&fit=crop&w=900&q=80",
            },
        ]

        for product in products:
            Product.objects.update_or_create(name=product["name"], defaults=product)

        Product.objects.exclude(name__in=[product["name"] for product in products]).delete()

        self.stdout.write(self.style.SUCCESS("Seeded products."))
