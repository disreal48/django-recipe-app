from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeSearchForm
from django.db.models import Q
import pandas as pd
from .utils import get_chart


def home(request):
    return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    paginate_by = 10
    ordering = ['name']

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'
  



def search_recipes(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if form.is_valid():
        if request.method == 'POST':
            recipe_name = form.cleaned_data.get('recipe_name')
            cooking_time = form.cleaned_data.get('cooking_time')
            difficulty = form.cleaned_data.get('difficulty')
            chart_type = form.cleaned_data.get('chart_type')

            query = Q()
            if recipe_name:
                query &= Q(name__icontains=recipe_name)
            if cooking_time is not None:
                query &= Q(cooking_time__lte=cooking_time)
            if difficulty:
                query &= Q(difficulty__icontains=difficulty)

            qs = Recipe.objects.filter(query)
                
            qs2 = [
                recipe
                for recipe in Recipe.objects.all()
                if recipe.difficulty == difficulty
            ]

            qs3 = Recipe.objects.filter(pk__in={recipe.pk for recipe in qs2})

            qs = (qs | qs3).distinct()

            if qs.exists():
                recipes_df = pd.DataFrame(qs.values("name", "cooking_time"))
                recipes_df['difficulty'] = [recipe.difficulty for recipe in qs]

                chart = get_chart(
                    chart_type, 
                    recipes_df, 
                    labels=recipes_df["name"].values,
                    x_label='Recipe Name',
                    y_label='Cooking Time (minutes)'
                )

                recipes_df_html = recipes_df.to_html(index=False)

                recipes_df_html = recipes_df_html.replace('<th>name</th>', '<th>Name</th>')
                recipes_df_html = recipes_df_html.replace('<th>cooking_time</th>', '<th>Cooking Time</th>')
                recipes_df_html = recipes_df_html.replace('<th>difficulty</th>', '<th>Difficulty</th>')

                recipes_df = recipes_df_html

    return render(request, 'recipes/recipes_search.html', {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart
    })