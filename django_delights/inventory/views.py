from datetime import datetime, timedelta
from django.template.defaultfilters import date as _date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from inventory.models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm
from django.contrib import messages

# Create your views here.
def home(request):
  context = {"name": request.user.username}
  return render(request, "inventory/home.html", context)

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
    recipe_requirements  = RecipeRequirement.objects.filter(menu_item = menu_item)
    errors_list = []
    for i in recipe_requirements:
      if (i.ingredient.quantity - i.quantity) >= 0:
        pass
      else:
        errors_list.append(i.ingredient.name)
    if (errors_list.__len__() == 0):
      i.ingredient.quantity -= i.quantity
      i.ingredient.save()
      item.save()
      messages.success(self.request, "successful")
      return super(PurchaseCreate, self).form_valid(form)
    else:
      error_string = ", ".join(errors_list)
      messages.error(self.request, f"not enough ingredients in the inventory! ({error_string})")
      return self.render_to_response(self.get_context_data(form=form))

# view the profit and revenue for the restaurant
def show_profit(request):
  # calculating total revenue for the restaurant’s overall recorded purchases
  total_revenue = 0
  purchases = Purchase.objects.all()
  for purchase in purchases:
    total_revenue += purchase.menu_item.price

  # calculating total cost for the restaurant's overall recorded purchases
  total_cost = 0
  purchases_menu = [purchase.menu_item for  purchase in purchases]

  recipe_requirements_list = []
  for item in purchases_menu:
    menu_items_list = RecipeRequirement.objects.filter(menu_item_id=item.id).values()
    for menu_item in menu_items_list:
      recipe_requirements_list.append(menu_item)

  for item in recipe_requirements_list:
    ingredient_id = item.get('ingredient_id')
    price = Ingredient.objects.get(id = ingredient_id).unit_price
    total_cost += price

  # calculating total profit (revenue - cost) of the restaurant
  total_profit = total_revenue - total_cost

  #calculating total revenue for the previous day:
  yesterday = datetime.now() - timedelta(days=1)
  time_string = yesterday.strftime("%Y-%m-%d")
  yesterday_purchases = Purchase.objects.filter(timestamp__contains = time_string)
  yesterday_revenue = 0
  for purchase in yesterday_purchases:
    yesterday_revenue += purchase.menu_item.price

  #calculating total profit for the previous day:
  yesterday_cost = 0
  yesterday_profit = 0
  yesterday_purchases_menu = [purchase.menu_item for purchase in yesterday_purchases]
  yesterday_recipe_requirements_list = []
  for item in yesterday_purchases_menu:
    menu_items_list = RecipeRequirement.objects.filter(menu_item_id=item.id).values()
    for menu_item in menu_items_list:
      yesterday_recipe_requirements_list.append(menu_item)

  for item in yesterday_recipe_requirements_list:
    ingredient_id = item.get('ingredient_id')
    price = Ingredient.objects.get(id = ingredient_id).unit_price
    yesterday_cost += price

  yesterday_profit = yesterday_revenue - yesterday_cost

  context = {"total_profit": total_profit,
            "total_revenue": total_revenue,
            "yesterday_revenue": yesterday_revenue,
            "yesterday_profit": yesterday_profit}
  return render(request, "inventory/balance.html", context)
