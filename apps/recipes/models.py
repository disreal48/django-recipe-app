from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(
        max_length=255, help_text="Enter ingredients comma separated"
    )
    cooking_time = models.IntegerField(help_text="Enter cooking time (minutes)")
    difficulty = None

    def __str__(self):
        return str(self.name)