from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeSearchForm
from django.db.models import Q
import pandas as pd


def home(request):
  return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
  model = Recipe
  template_name = 'recipes/recipes_list.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
  model = Recipe
  template_name = 'recipes/recipes_detail.html'
  

def search_recipes(request):
  form = RecipeSearchForm(request.POST or None)
  recipes_df = None
  chart = None
  
  if request.method =='POST':
    recipe_name = request.POST.get('recipe_name')
    cooking_time = request.POST.get('cooking_time')
    difficulty = request.POST.get('difficulty')
    chart_type = request.POST.get('chart_type')
    
    cooking_time = 0 if not cooking_time else cooking_time
    recipe_name = "" if not recipe_name else recipe_name
    difficulty = "" if not difficulty else difficulty   
    
    qs = Recipe.objects.filter(
              Q(name=recipe_name)  
              | Q(cooking_time=cooking_time)
          )
    
    qs2 = [
            recipe
            for recipe in Recipe.objects.all()
            if recipe.difficulty == difficulty
        ]  

    qs3 = Recipe.objects.filter(pk__in={recipe.pk for recipe in qs2})

    qs = (qs | qs3).distinct()
    
    if qs:
      recipes_df = pd.DataFrame(qs.values("name", "cooking_time"))
      recipes_df['difficulty'] = [recipe.difficulty for recipe in qs]
      

    print(recipes_df)
    
    recipes_df = recipes_df.to_html(index=False)

  
  
  
  
  
  context={
    'form': form,
    'recipes_df': recipes_df,
    # 'chart': chart
  }
  
  return render(request, 'recipes/recipes_search.html', context)