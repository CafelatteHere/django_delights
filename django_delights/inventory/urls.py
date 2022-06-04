from django.urls import path
from . import views

urlpatterns = [
  # path("", views.home, name="home"),
  path("ingredient/list", views.IngredientList.as_view(), name="ingredientlist"),
  path("ingredient/create", views.IngredientCreate.as_view(), name="ingredientcreate"),
]