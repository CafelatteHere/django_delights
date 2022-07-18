from datetime import datetime, timedelta
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from inventory.models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class UserLogin(LoginView):
  template_name = "registration/login.html"
  success_url = "home"

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"

def logout_view(request):
  logout(request)
  return redirect("login")

@login_required
def home(request):
  context = {"name": request.user.username}
  return render(request, "inventory/home.html", context)

class IngredientList(LoginRequiredMixin, ListView):
  ingredients = Ingredient.objects.all()
  context = {"ingredients": ingredients}
  model = Ingredient
  template_name = "inventory/ingredient_list.html"

class IngredientCreate(LoginRequiredMixin, CreateView):
  model = Ingredient
  template_name = "inventory/ingredient_create_form.html"
  form_class = IngredientForm

class IngredientDetail(LoginRequiredMixin, DetailView):
  model = Ingredient
  template_name = "inventory/ingredient_details.html"
  # ingredient =  Ingredient.objects.get(ingredient_id=self.object.id)
  # recipe_requirements_list = []
  # recipe_requirements = ingredient.reciperequirement_set.all()
  # for item in recipe_requirements:
  #   recipe_requirements_list.append(item)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['object'] = self.object
    ingredient = Ingredient.objects.get(id=context['object'].pk)
    recipe_requirements_list = []
    for item in context['object'].reciperequirement_set.all():
      recipe_requirements_list.append(item)
    context = {
      'ingredient':ingredient,
      'recipe_requirements_list': recipe_requirements_list
    }
    return context
  # items = get_object(self).reciperequirement_set.all()
  # context =  {"items": items}


class IngredientUpdate(LoginRequiredMixin, UpdateView):
  model = Ingredient
  template_name = "inventory/ingredient_update_form.html"
  form_class = IngredientForm

class IngredientDelete(LoginRequiredMixin, DeleteView):
  model = Ingredient
  template_name = "inventory/ingredient_delete_form.html"
  success_url = "/ingredient/list"

class MenuItemList(LoginRequiredMixin, ListView):
  model = MenuItem
  template_name = "inventory/menuitem_list.html"

class MenuItemCreate(LoginRequiredMixin, CreateView):
  model = MenuItem
  template_name = "inventory/menuitem_create.html"
  form_class = MenuItemForm

class MenuItemDetail(LoginRequiredMixin, DetailView):
  model = MenuItem
  template_name = "inventory/menuitem_details.html"

  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)

class MenuItemUpdate(LoginRequiredMixin, UpdateView):
  model = MenuItem
  template_name = "inventory/menuitem_update_form.html"
  form_class = MenuItemForm

class MenuItemDelete(LoginRequiredMixin, DeleteView):
  model = MenuItem
  template_name = "inventory/menuitem_delete_form.html"
  success_url = "/menuitem/list"

class PurchaseList(LoginRequiredMixin, ListView):
  model = Purchase
  template_name = "inventory/purchase_list.html"

class PurchaseCreate(LoginRequiredMixin, CreateView):
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
@login_required
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
