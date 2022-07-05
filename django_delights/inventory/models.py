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

  def __str__(self):
    return f"{self.name}: {self.unit_price} {self.unit}"

  def get_absolute_url(self):
    return "/ingredient/list"

# represents an item on the restaurant’s menu
class MenuItem(models.Model):
  title = models.CharField(max_length=50, unique=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"{self.title}, price: {self.price}"

  def get_absolute_url(self):
    return "/menuitem/list"

# represents a single ingredient and how much of it is required for an item on the menu
class RecipeRequirement(models.Model):
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
  quantity = models.DecimalField(max_digits=7, decimal_places=1)
  unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="")

  def __str__(self):
    return f"menu item: {self.menu_item}, ingredient: {self.ingredient}"

class Purchase(models.Model):
  timestamp = models.DateTimeField(auto_now_add=True)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)

  def get_absolute_url(self):
    return "/purchase/list"

  def __str__(self):
    return f"{self.menu_item} was purchased at {self.timestamp}"
