# apps/recipes/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name="Pasta",
            ingredients="Spaghetti, Tomatoes, Cheese",
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

class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Recipe.objects.create(
            name="Pasta",
            ingredients="Spaghetti, Tomatoes, Cheese",
            cooking_time=11,
            pic='recipes/no_picture.jpg'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_search_recipes_view(self):
        response = self.client.get(reverse('recipes:recipes_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_search.html')

    def test_search_recipes_view_post(self):
        response = self.client.post(reverse('recipes:recipes_search'), {
            'recipe_name': 'Pasta',
            'cooking_time': '',
            'difficulty': '',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta')

    def test_search_fields_validation(self):
        response = self.client.post(reverse('recipes:recipes_search'), {
            'recipe_name': 'A' * 121,  # Exceeding max length
            'cooking_time': 'invalid',  # Invalid format
            'difficulty': 'InvalidChoice',  # Invalid choice
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'recipe_name', 'Ensure this value has at most 120 characters (it has 121).')
        self.assertFormError(response, 'form', 'cooking_time', 'Enter a whole number.')
        self.assertFormError(response, 'form', 'difficulty', 'Select a valid choice. InvalidChoice is not one of the available choices.')

    def test_login_protection(self):
        self.client.logout()
        response = self.client.get(reverse('recipes:recipes_list'))
        login_url = reverse('user:login_view')
        self.assertRedirects(response, f"{login_url}?next={reverse('recipes:recipes_list')}")

    def test_pagination(self):
        for i in range(15):
            Recipe.objects.create(
                name=f"Recipe {i}",
                ingredients="Ingredient1, Ingredient2",
                cooking_time=10,
                pic='recipes/no_picture.jpg'
            )
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['recipe_list']), 10)  # Assuming pagination is set to 10 per page