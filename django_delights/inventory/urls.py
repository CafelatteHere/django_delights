from django.urls import path
from . import views

urlpatterns = [
  # path("", views.home, name="home"),
  path("ingredient/list", views.IngredientList.as_view(), name="ingredientlist"),
  path("ingredient/create", views.IngredientCreate.as_view(), name="ingredientcreate"),
  path("ingredient/<pk>", views.IngredientDetail.as_view(), name="ingredientdetails"),
  path("ingredient/<pk>/update", views.IngredientUpdate.as_view(), name="ingredientupdate"),
  path("ingredient/<pk>/delete", views.IngredientDelete.as_view(), name="ingredientdelete"),
]