# Generated by Django 4.0.4 on 2022-05-22 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=7)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('unit', models.CharField(choices=[('g', 'gram'), ('tbsp', 'tablespoon'), ('tsp', 'teaspoon'), ('l', 'liter'), ('cup', 'cup'), ('', '')], default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(choices=[('g', 'gram'), ('tbsp', 'tablespoon'), ('tsp', 'teaspoon'), ('l', 'liter'), ('cup', 'cup'), ('', '')], default='', max_length=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.ingredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.menuitem')),
            ],
        ),
    ]
