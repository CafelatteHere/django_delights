# from pyexpat import model
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from inventory.models import Ingredient, MenuItem
from .forms import IngredientForm

# Create your views here.
class IngredientList(ListView):
  ingredients = Ingredient.objects.all()
  context = {"ingredients": ingredients}
  model = Ingredient
  template_name = "inventory/ingredient_list.html"

class IngredientCreate(CreateView):
  model = Ingredient
  template_name = "inventory/ingredient_create_form.html"
  form_class = IngredientForm

class IngredientDetail(DetailView):
  model = Ingredient
  template_name = "inventory/ingredient_details.html"

  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)


class IngredientUpdate(UpdateView):
  model = Ingredient
  template_name = "inventory/ingredient_update_form.html"
  form_class = IngredientForm

class IngredientDelete(DeleteView):
  model = Ingredient
  template_name = "inventory/ingredient_delete_form.html"
  success_url = "/ingredient/list"

class MenuItemList(ListView):
  model = MenuItem
  template_name = "inventory/menuitem_list.html"
