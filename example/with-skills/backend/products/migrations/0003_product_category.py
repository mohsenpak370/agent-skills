from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_cart_cartitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[
                    ("men", "Men"),
                    ("women", "Women"),
                    ("kids", "Kids"),
                    ("accessories", "Accessories"),
                ],
                default="men",
                max_length=24,
            ),
        ),
    ]
