from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Create sample clothing products for local development."

    def handle(self, *args, **options):
        products = [
            {
                "name": "Relaxed Linen Shirt",
                "description": "Breathable linen shirt with a soft drape for warm days.",
                "category": Product.Category.MEN,
                "brand": "Northline",
                "size": "S - XL",
                "color": "Ivory",
                "price": "48.00",
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "name": "Tailored Everyday Blazer",
                "description": "Clean-cut blazer that works from office hours to dinner plans.",
                "category": Product.Category.MEN,
                "brand": "Atelier Row",
                "size": "M - XXL",
                "color": "Charcoal",
                "price": "129.00",
                "image_url": "https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
            {
                "name": "Soft Knit Polo",
                "description": "Textured polo with a modern open collar and relaxed fit.",
                "category": Product.Category.MEN,
                "brand": "Sunday Supply",
                "size": "S - XL",
                "color": "Sage",
                "price": "42.50",
                "image_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
            {
                "name": "Satin Midi Dress",
                "description": "Fluid midi dress with an elegant neckline and evening-ready shine.",
                "category": Product.Category.WOMEN,
                "brand": "Maison Vale",
                "size": "XS - L",
                "color": "Copper",
                "price": "96.00",
                "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "name": "Wide Leg Denim",
                "description": "High-rise jeans made with structured denim and a roomy leg.",
                "category": Product.Category.WOMEN,
                "brand": "Blue Form",
                "size": "24 - 34",
                "color": "Vintage Blue",
                "price": "74.00",
                "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
            {
                "name": "Cropped Trench Jacket",
                "description": "Lightweight cropped trench with storm flaps and a cinched waist.",
                "category": Product.Category.WOMEN,
                "brand": "Harbor Studio",
                "size": "XS - XL",
                "color": "Sand",
                "price": "118.00",
                "image_url": "https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "name": "Kids Rainbow Hoodie",
                "description": "Cozy fleece hoodie with playful color blocking for everyday adventures.",
                "category": Product.Category.KIDS,
                "brand": "Little Loop",
                "size": "2Y - 10Y",
                "color": "Rainbow",
                "price": "36.00",
                "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "name": "Kids Denim Overalls",
                "description": "Durable overalls with adjustable straps and roomy pockets.",
                "category": Product.Category.KIDS,
                "brand": "Mini Works",
                "size": "3Y - 9Y",
                "color": "Denim",
                "price": "44.00",
                "image_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
            {
                "name": "Canvas Weekender Tote",
                "description": "Oversized cotton canvas tote for market days, gym trips, and weekends.",
                "category": Product.Category.ACCESSORIES,
                "brand": "Carry Co.",
                "size": "One Size",
                "color": "Natural",
                "price": "39.00",
                "image_url": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "name": "Ribbed Beanie",
                "description": "Soft ribbed beanie for cold-weather layers and casual styling.",
                "category": Product.Category.ACCESSORIES,
                "brand": "Wool & Co",
                "size": "One Size",
                "color": "Oatmeal",
                "price": "22.00",
                "image_url": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
        ]

        Product.objects.filter(name__in=["Classic Backpack", "Desk Lamp", "Ceramic Mug"]).delete()

        for data in products:
            Product.objects.update_or_create(name=data["name"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Sample clothing products are ready."))
