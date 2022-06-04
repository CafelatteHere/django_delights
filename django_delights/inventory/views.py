from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from inventory.models import Ingredient
from .forms import IngredientCreateForm

# Create your views here.
class IngredientList(ListView):
  ingredients = Ingredient.objects.all()
  context = {"ingredients": ingredients}
  model = Ingredient
  template_name = "inventory/ingredient_list.html"

class IngredientCreate(CreateView):
  model = Ingredient
  template_name = "inventory/ingredient_create_form.html"
  form_class = IngredientCreateForm