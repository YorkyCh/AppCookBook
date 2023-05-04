from django.db import models
from django.core.validators import RegexValidator

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

SPICINESS_CHOICES = (
    (1, 'Mild'),
    (2, 'Medium'),
    (3, 'Hot'),
    (4, 'Very Hot'),
    (5, 'Extremely Hot')
)


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    preparation_time = models.PositiveIntegerField()
    category = models.CharField(max_length=200, default='Unknown')
    cook_time = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/', default='default_image.png')
    spiciness = models.IntegerField(choices=SPICINESS_CHOICES, default=1)
    steps = models.TextField(default='')
    ingredients = models.ManyToManyField(Ingredient)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name



class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.recipe.name}: {self.amount} {self.ingredient.name}"

class MeasurementUnit(models.Model):
    name = models.CharField(max_length=100)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_amounts')

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} {self.unit.name}'