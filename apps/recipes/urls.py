from django.urls import path
from .views import home
from .views import search_recipes
from .views import RecipeListView, RecipeDetailView

app_name = 'recipes' 

urlpatterns = [
  path('', home, name='home'),
  path('recipes/', RecipeListView.as_view(), name='recipes_list'),
  path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipes_detail'),
  path('search/', search_recipes, name='recipes_search'),
]