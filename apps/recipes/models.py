from django.db import models
from apps.core.abstracts.models import CreatedModifiedAbstract

# Create your models here.

class Recipe(CreatedModifiedAbstract):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(
        max_length=255, help_text="Enter ingredients comma separated"
    )
    cooking_time = models.IntegerField(help_text="Enter cooking time (minutes)")

    @property
    def difficulty(self):
      ingredients_len = len(self.return_ingredients_as_list())
      if self.cooking_time < 10 and ingredients_len < 4:
        return "Easy"
      elif self.cooking_time < 10 and ingredients_len >= 4:
        return "Medium"
      elif self.cooking_time >= 10 and ingredients_len < 4:
        return "Intermediate"
      else:
        return "Hard"
    
    def return_ingredients_as_list(self):
        return self.ingredients.split(', ') if self.ingredients else []

    def __str__(self):
        return f"{self.name} - {self.difficulty} - {self.cooking_time}"