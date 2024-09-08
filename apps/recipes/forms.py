from django import forms

CHART__CHOICES = (        
  ('#1', 'Bar chart'),    
  ('#2', 'Pie chart'),
  ('#3', 'Line chart')
)

DIFFICULTY_CHOICES = (
    ("", "select"),
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Intermediate", "Intermediate"),
    ("Hard", "Hard"),
)

class RecipeSearchForm(forms.Form): 
  recipe_name = forms.CharField(max_length=120, required=False)
  cooking_time = forms.IntegerField(required=False)
  difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)
  chart_type = forms.ChoiceField(choices=CHART__CHOICES)