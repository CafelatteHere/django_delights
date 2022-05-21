from django.db import models

# Create your models here.
class Ingredient(models.Model):
  UNIT_CHOICES = [
    ("g", "gram"),
    ("tbsp", "tablespoon"),
    ("tsp", "teaspoon"),
    ("l", "liter"),
    ("cup", "cup"),
    ("", "")
  ]
  name = models.CharField(max_length=30, unique=True)
  quantity = models.DecimalField(max_digits=7, decimal_places=1)
  unit_price = models.DecimalField(max_digits=7, decimal_places=2)
  unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="")

class RecipeRequirement(models.Model):
  name = models.CharField(max_length=40, unique=True)
  ingredient = models.ManyToManyField(Ingredient)

class MenuItem(models.Model):
  name = models.CharField(max_length=50, unique=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  recipe = models.ForeignKey(RecipeRequirement, on_delete=models.CASCADE)

class Purchase(models.Model):
  timestamp = models.DateField(auto_now_add=True)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)