from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, RecipeIngredient, Category

class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            preparation_time=30,
            cook_time=60,
            description='Test description',
            spiciness=2,
            steps="1. Step one\n2. Step two"
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount="2 cups"
        )
        self.recipe.categories.set([Category.objects.create(name='Test Category')])

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_name = 'Test Recipe'
        self.assertEqual(recipe.name, expected_name)

    def test_recipe_preparation_time(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.preparation_time, 30)

    def test_recipe_cook_time(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.cook_time, 60)

    def test_recipe_spiciness(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.spiciness, 2)

    def test_recipe_description(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_description = 'Test description'
        self.assertEqual(recipe.description, expected_description)

    def test_recipe_steps(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_steps = '1. Step one\n2. Step two'
        self.assertEqual(recipe.steps, expected_steps)

    def test_recipe_ingredients(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_ingredient = self.ingredient
        self.assertEqual(recipe.recipeingredient_set.first().ingredient, expected_ingredient)

    def test_recipe_ingredient_amount(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_amount = '2 cups'
        self.assertEqual(recipe.recipeingredient_set.first().amount, expected_amount)

    def test_recipe_categories(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_category_name = 'Test Category'
        self.assertEqual(recipe.categories.first().name, expected_category_name)
