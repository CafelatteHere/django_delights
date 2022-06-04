from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

class IngredientCreateForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = "__all__"

class IngredientUpdateForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = "__all__"