import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cookbook_project.settings'
django.setup()

from cookbook_app.models import Ingredient, Category, MeasurementUnit, Recipe, RecipeIngredient

ingredients = [
    "Avocado",
    "Beans (black, pinto, kidney, etc.)",
    "Bell peppers",
    "Cilantro",
    "Corn",
    "Garlic",
    "Jalapeño peppers",
    "Limes",
    "Onions",
    "Tomatoes",
    "Ancho chiles",
    "Cheddar cheese",
    "Chicken",
    "Chipotle peppers",
    "Cinnamon",
    "Cumin",
    "Lime juice",
    "Oregano",
    "Paprika",
    "Pork",
    "Red pepper flakes",
    "Serrano peppers",
    "Shrimp",
    "Sour cream",
    "Tortillas",
    "Adobo sauce",
    "Almonds",
    "Anaheim chiles",
    "Annatto",
    "Avocado oil",
    "Bay leaves",
    "Beef",
    "Cactus (nopales)",
    "Carrots",
    "Chayote",
    "Chile de arbol",
    "Cilantro leaves",
    "Cocoa powder",
    "Coconut milk",
    "Cotija cheese",
    "Cranberries",
    "Epazote",
    "Fajita seasoning",
    "Fish (tilapia, cod, etc.)",
    "Guajillo chiles",
    "Habanero peppers",
    "Honey",
    "Jicama",
    "Masa harina",
    "Mexican crema",
    "Mexican oregano",
    "Mushrooms",
    "Orange juice",
    "Panela cheese",
    "Pasilla chiles",
    "Pineapple",
    "Plantains",
    "Queso fresco",
    "Radishes",
    "Refried beans",
    "Rice",
    "Roasted red peppers",
    "Salsa",
    "Sazon seasoning",
    "Sesame seeds",
    "Smoked paprika",
    "Squash (zucchini, yellow squash, etc.)",
    "Steak",
    "Sweet potatoes",
    "Tamarind paste",
    "Tostadas",
    "Turkey",
    "Vanilla extract",
    "White cheese (queso blanco)",
    "White onion",
    "Yellow onion",
    "Achiote paste",
    "Agave nectar",
    "Al pastor seasoning",
    "Apple cider vinegar",
    "Avocado leaves",
    "Banana leaves",
    "Beef stock",
    "Black beans",
    "Brown sugar",
    "Cactus fruit (tuna)",
    "Calabacitas",
    "Cascabel chiles",
    "Chihuahua cheese",
    "Chopped green chiles",
    "Chorizo",
    "Clams",
    "Coconut flakes",
    "Cream cheese",
    "Dried shrimp",
    "Enchilada sauce",
    "Flour tortillas",
    "Fried pork rinds (chicharrones)",
    "Ground beef",
    "Hoja santa"
]

categories = [
    'Vegetarian',
    'Vegan',
    'Gluten-free',
    'Low-carb',
]

measurement_units = [
    'grams',
    'milligrams',
    'kilograms',
    'ounces',
    'pounds',
    'milliliters',
    'liters',
    'teaspoons',
    'tablespoons',
    'cups',
    'pints',
    'quarts',
    'gallons',
]

# Create Categories
for category_name in categories:
    Category.objects.get_or_create(name=category_name)

# Create Ingredients
for ingredient_name in ingredients:
    Ingredient.objects.get_or_create(name=ingredient_name)

# Create MeasurementUnits
for unit_name in measurement_units:
    MeasurementUnit.objects.get_or_create(name=unit_name)

recipes = [
    {
        'name': 'Recipe 1',
        'description': 'Description of Recipe 1',
        'preparation_time': 30,
        'image': 'default_image.jpg',
        'spiciness': 2,
        'steps': 'Step 1\nStep 2\nStep 3',
        'portion_size': 4,
        'categories': ['Vegetarian', 'Low-carb'],
        'ingredients': [
            {'ingredient': 'Avocado', 'amount': '200', 'unit': 'grams'},
            {'ingredient': 'Beans (black, pinto, kidney, etc.)', 'amount': '2', 'unit': 'cups'},
        ]
    },
    {
        'name': 'Recipe 2',
        'description': 'Description of Recipe 2',
        'preparation_time': 45,
        'image': 'default_image.jpg',
        'spiciness': 3,
        'steps': 'Step 1\nStep 2\nStep 3',
        'portion_size': 2,
        'categories': ['Vegan', 'Gluten-free'],
        'ingredients': [
            {'ingredient': 'Corn', 'amount': '500', 'unit': 'grams'},
            {'ingredient': 'Garlic', 'amount': '1', 'unit': 'teaspoon'},
        ]
    },
    # Add more recipes as needed
]

for recipe_data in recipes:
    recipe = Recipe(
        name=recipe_data['name'],
        description=recipe_data['description'],
        preparation_time=recipe_data['preparation_time'],
        image=recipe_data['image'],
        spiciness=recipe_data['spiciness'],
        steps=recipe_data['steps'],
        portion_size=recipe_data['portion_size'],
    )
    recipe.save()

    for category_name in recipe_data['categories']:
        category = Category.objects.get(name=category_name)
        recipe.categories.add(category)

    for ingredient_data in recipe_data['ingredients']:
        ingredient = Ingredient.objects.get(name=ingredient_data['ingredient'])
        amount = ingredient_data['amount']
        unit_name = ingredient_data['unit']
        unit, _ = MeasurementUnit.objects.get_or_create(name=unit_name)

        recipe_ingredient = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount,
            unit=unit,
        )
        recipe_ingredient.save()
