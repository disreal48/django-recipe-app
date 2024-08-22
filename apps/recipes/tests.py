from django.test import TestCase
from .models import Recipe

# Create your tests here.

class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name="Pasta",
            ingredients="Spagehtti, Tomatoes, Cheese",
            cooking_time=11,
        )

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")
        
    def test_name_value(self):
        recipe = Recipe.objects.get(id=1)
        name_value = recipe.name
        self.assertIsInstance(name_value, str)

    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)
        
    def test_ingredients_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("ingredients").verbose_name
        self.assertEqual(field_label, "ingredients")
        
    def test_ingredients_value(self):
        recipe = Recipe.objects.get(id=1)
        ingredients_value = recipe.ingredients
        self.assertIsInstance(ingredients_value, str)

    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredients").max_length
        self.assertEqual(max_length, 255)

    def test_cooking_time_value(self):
        recipe = Recipe.objects.get(id=1)
        cooking_time_value = recipe.cooking_time
        self.assertIsInstance(cooking_time_value, int)
        
    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/recipes/1/')