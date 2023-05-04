import os
import django
import sys

sys.path.append('/home/mploig/developer/Mexican_cookbook/cookbook_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cookbook_project.settings'
django.setup()

from cookbook_app.models import Ingredient, Category, MeasurementUnit

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
    ('g', 'grams', 1),
    ('mg', 'milligrams', 0.001),
    ('kg', 'kilograms', 1000),
    ('oz', 'ounces', 28.35),
    ('lb', 'pounds', 453.592),
    ('ml', 'milliliters', 1),
    ('l', 'liters', 1000),
    ('tsp', 'teaspoons', 4.929),
    ('tbsp', 'tablespoons', 14.787),
    ('cup', 'cups', 240),
    ('pt', 'pints', 473.176),
    ('qt', 'quarts', 946.353),
    ('gal', 'gallons', 3785.41),
]

for unit, unit_name, conversion_rate in measurement_units:
    MeasurementUnit.objects.get_or_create(name=unit_name, conversion_rate=conversion_rate)

for ingredient_name in ingredients:
    Ingredient.objects.get_or_create(name=ingredient_name)

for category_name in categories:
    Category.objects.get_or_create(name=category_name)
