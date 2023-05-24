from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe, Ingredient, RecipeIngredient, Category, MeasurementUnit
from .forms import RecipeForm
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.measurement_unit = MeasurementUnit.objects.create(name='Cup')
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            preparation_time=30,
            description='Test description',
            spiciness=2,
            steps="1. Step one\n2. Step two",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            portion_size=2,
            base_portion_size=2,
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount="2",
            unit=self.measurement_unit
        )
        self.recipe.categories.set([Category.objects.create(name='Test Category')])

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_name = 'Test Recipe'
        self.assertEqual(recipe.name, expected_name)

    def test_recipe_preparation_time(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.preparation_time, 30)

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
        expected_amount = '2'
        self.assertEqual(recipe.recipeingredient_set.first().amount, expected_amount)

    def test_recipe_categories(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_category_name = 'Test Category'
        self.assertEqual(recipe.categories.first().name, expected_category_name)

    def test_recipe_image(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        expected_image = 'test_image.jpg'
        self.assertTrue(recipe.image.name.startswith('test_image'))

    def test_recipe_portion_size(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.portion_size, 2)

    def test_recipe_base_portion_size(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.base_portion_size, 2)


class RecipeFormTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

    def test_valid_data(self):
        image_content = BytesIO()
        image_file = Image.new('RGB', size=(100, 100), color=(255, 0, 0))
        image_file.save(image_content, 'jpeg')
        image_content.seek(0)
        image = SimpleUploadedFile(name='test_image.jpg', content=image_content.read(), content_type='image/jpeg')

        form = RecipeForm(
            data={
                'name': 'Test Recipe',
                'description': 'Test description',
                'preparation_time': 30,
                'spiciness': 2,
                'steps': '1. Step one\n2. Step two',
                'categories': [self.category.id],
                'portion_size': 2,
                'base_portion_size': 2,
            },
            files={'image': image}
        )
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = RecipeForm({})


        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'description': ['This field is required.'],
            'preparation_time': ['This field is required.'],
            'spiciness': ['This field is required.'],
            'steps': ['This field is required.'],
            'image': ['This field is required.'],
            'portion_size': ['This field is required.'],
            'base_portion_size': ['This field is required.'],
        })


class RecipeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        image_content = BytesIO()
        image_file = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image_file.save(image_content, 'png')
        image_content.seek(0)
        self.image = SimpleUploadedFile(name='test_image.png', content=image_content.read(), content_type='image/png')

        # Now create the Recipe object
        self.recipe = Recipe.objects.create(
            id=1,
            name='Test Recipe',
            description='Test description',
            preparation_time=30,
            spiciness=2,
            steps='1. Step one\n2. Step two',
            image=self.image,
            portion_size=2,
            base_portion_size=2,  # use the image created above
        )
        self.recipe.categories.set([self.category])

    def test_add_recipe_view(self):
        url = reverse('add_recipe')
        image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image.jpg', 'rb').read(), content_type='image/jpeg')

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_recipe.html')
        self.assertIsInstance(response.context['form'], RecipeForm)

        # Test POST request
        post_data = {
            'name': 'Test Recipe',
            'description': 'Test description',
            'preparation_time': 30,
            'spiciness': 2,
            'steps': '1. Step one\n2. Step two',
            'categories': [self.category.id],
            'portion_size': 2,
            'base_portion_size': 2,
            'image': image,
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)  # should redirect after successful form submission
        self.assertTrue(Recipe.objects.filter(name='Test Recipe').exists())  # check that the recipe was added to the database

    def test_update_recipe_view(self):
        url = reverse('update_recipe', args=[self.recipe.id])

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_recipe.html')
        self.assertIsInstance(response.context['form'], RecipeForm)

        # Test POST request
        post_data = {
            'name': 'Updated Test Recipe',
            'description': 'Updated Test description',
            'preparation_time': 40,
            'spiciness': 3,
            'steps': '1. Updated Step one\n2. Updated Step two',
            'categories': [self.category.id],
            'portion_size': 3,
            'base_portion_size': 3,
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.recipe.refresh_from_db()  # refresh the recipe instance to pull the updated data
        self.assertEqual(self.recipe.name, 'Updated Test Recipe')  # check that the recipe was updated in the database

    def test_delete_recipe_view(self):
        url = reverse('delete_recipe', args=[self.recipe.id])

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # should redirect after deleting the recipe
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())  # check that the recipe was deleted from the database

    def test_recipe_detail_view(self):
        url = reverse('recipe_detail', args=[self.recipe.id])

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertEqual(response.context['recipe'], self.recipe)  # check that the correct recipe instance is passed to the template

        # Test POST request
        post_data = {
            'portion_size': 2
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.recipe.refresh_from_db()  # refresh the recipe instance to pull the updated data
        self.assertEqual(self.recipe.portion_size, 2)  # check that the recipe's portion_size was updated in the database


class RecipeImageTestCase(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test description',
            preparation_time=30,
            spiciness=2,
            steps='1. Step one\n2. Step two',
            image=self.image
        )

    def test_image_file(self):
        self.assertTrue(self.recipe.image.name.startswith('test_image'))
