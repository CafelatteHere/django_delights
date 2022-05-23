from django.db import models

UNIT_CHOICES = [
  ("g", "gram"),
  ("tbsp", "tablespoon"),
  ("tsp", "teaspoon"),
  ("l", "liter"),
  ("cup", "cup"),
  ("oz", "ounces"),
  ("lbs", "pound"),
  ("", "")
]

# Create your models here.
class Ingredient(models.Model):
  name = models.CharField(max_length=30, unique=True)
  quantity = models.DecimalField(max_digits=7, decimal_places=1)
  unit_price = models.DecimalField(max_digits=7, decimal_places=2)
  unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="")

# represents an item on the restaurant’s menu
class MenuItem(models.Model):
  title = models.CharField(max_length=50, unique=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)

# represents a single ingredient and how much of it is required for an item off the menu
class RecipeRequirement(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
  quantity = models.CharField(max_length=10, choices=UNIT_CHOICES, default="")

class Purchase(models.Model):
  timestamp = models.DateTimeField(auto_now_add=True)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)