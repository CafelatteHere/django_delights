from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from inventory.models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm
from django.contrib import messages

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

class MenuItemCreate(CreateView):
  model = MenuItem
  template_name = "inventory/menuitem_create.html"
  form_class = MenuItemForm

class MenuItemDetail(DetailView):
  model = MenuItem
  template_name = "inventory/menuitem_details.html"

  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)

class MenuItemUpdate(UpdateView):
  model = MenuItem
  template_name = "inventory/menuitem_update_form.html"
  form_class = MenuItemForm

class MenuItemDelete(DeleteView):
  model = MenuItem
  template_name = "inventory/menuitem_delete_form.html"
  success_url = "/menuitem/list"

class PurchaseList(ListView):
  model = Purchase
  template_name = "inventory/purchase_list.html"

class PurchaseCreate(CreateView):
  model = Purchase
  form_class = PurchaseForm
  template_name = "inventory/purchase_create.html"

  # decreasing ingredient.quantity because ingredients were used for the purchased menu_item.
  def form_valid(self, form):
    item = form.save(commit=False)
    menu_item = MenuItem.objects.get(id = item.menu_item.id)
    item.save()
    recipe_requirements  = RecipeRequirement.objects.filter(menu_item = menu_item)
    for i in recipe_requirements:
      i.ingredient.quantity -= i.quantity
      i.ingredient.save()
    messages.success(self.request, "successful")
    return super(PurchaseCreate, self).form_valid(form)

