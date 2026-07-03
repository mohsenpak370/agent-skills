from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_cart_cartitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(choices=[("men", "Men"), ("women", "Women"), ("kids", "Kids"), ("accessories", "Accessories")], default="women", max_length=20),
        ),
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name="product",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
