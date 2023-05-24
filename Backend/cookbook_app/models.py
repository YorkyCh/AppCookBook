from django.db import models

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
    categories = models.ManyToManyField(Category)  # Add a many-to-many relationship with Category
    image = models.ImageField(upload_to='', default='default_image.png')
    spiciness = models.IntegerField(choices=SPICINESS_CHOICES, default=1)
    steps = models.TextField(default='')
    portion_size = models.IntegerField(default=1)
    base_portion_size = models.IntegerField(default=1)  


    def __str__(self):
        return self.name





class MeasurementUnit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)  # Update to use ForeignKey

    def __str__(self):
        return f"{self.recipe.name}: {self.amount} {self.unit}"
    
class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # Changed to DecimalField
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_amounts')

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} {self.unit.name}'
