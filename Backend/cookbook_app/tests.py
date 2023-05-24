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
        self.measurement_unit = MeasurementUnit.objects.create(name='Cup', conversion_rate=1)
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            preparation_time=30,
            description='Test description',
            spiciness=2,
            steps="1. Step one\n2. Step two",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
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
            image=self.image  # use the image created above
        )
        self.recipe.categories.set([self.category])

    def test_add_recipe_view(self):
        url = reverse('add_recipe')

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_recipe.html')  # assuming that 'add_recipe.html' is the correct template
        self.assertIsInstance(response.context['form'], RecipeForm)  # check that a RecipeForm instance is passed to the template

        # Test POST request
        post_data = {
            'name': 'Test Recipe',
            'description': 'Test description',
            'preparation_time': 30,
            'spiciness': 2,
            'steps': '1. Step one\n2. Step two',
            'categories': [self.category.id]
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)  # should redirect after successful form submission
        self.assertTrue(Recipe.objects.filter(name='Test Recipe').exists())  # check that the recipe was added to the database

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
