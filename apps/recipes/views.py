from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeSearchForm
from django.db.models import Q
import pandas as pd
from .utils import get_chart
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def home(request):
    return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    paginate_by = 30
    ordering = ['name']

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'
  

@login_required
def search_recipes(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST' and form.is_valid():
        recipe_name = form.cleaned_data.get('recipe_name')
        cooking_time = form.cleaned_data.get('cooking_time')
        difficulty = form.cleaned_data.get('difficulty')
        chart_type = form.cleaned_data.get('chart_type')

        q = Q()
        if recipe_name:
            q &= Q(name__icontains=recipe_name)
        if cooking_time is not None:
            q &= Q(cooking_time=cooking_time)

        qs = Recipe.objects.filter(q)

        if difficulty:
            qs = [recipe for recipe in qs if recipe.difficulty == difficulty]

        if qs:
            recipes_df = pd.DataFrame([{
                'name': recipe.name,
                'cooking_time': recipe.cooking_time,
                'difficulty': recipe.difficulty
            } for recipe in qs])

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
            
            for q in qs:
                item_id = q.id
                item_name = q.name  

                recipes_df = recipes_df.replace( 
                    f"<td>{item_name}</td>",
                    f"<td><a href='{reverse('recipes:recipes_detail', kwargs={'pk': item_id})}' style='text-decoration: none'>{item_name}</a></td>",
                )

    return render(request, 'recipes/recipes_search.html', {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart
    })