from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, inlineformset_factory
from .models import Recipe, Ingredient, Category, IngredientAmount, MeasurementUnit, RecipeIngredient
from .forms import RecipeForm, IngredientAmountForm, RecipeIngredientForm
from django.db.models import Q 
from django.forms.widgets import CheckboxSelectMultiple


def add_recipe(request):
    RecipeIngredientFormSet = inlineformset_factory(
        Recipe,
        RecipeIngredient,
        form=RecipeIngredientForm,
        fields=('ingredient', 'amount', 'unit'),
        extra=1
    )

    categories = Category.objects.all()  # Retrieve categories

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', queryset=RecipeIngredient.objects.none())

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            recipe.categories.set(request.POST.getlist('categories'))

            for ingredient_form in formset:
                if ingredient_form.cleaned_data:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            return redirect('recipe_detail', recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(prefix='ingredients', queryset=RecipeIngredient.objects.none())

    return render(request, 'add_recipe.html', {
        'form': form,
        'formset': formset,
        'categories': categories,
    })


import logging

logger = logging.getLogger(__name__)


def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    RecipeIngredientFormSet = inlineformset_factory(
        Recipe,
        RecipeIngredient,
        form=RecipeIngredientForm,
        fields=('ingredient', 'amount', 'unit'),
        extra=1
    )

    categories = Category.objects.all()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        form.fields['categories'].widget = CheckboxSelectMultiple()  # Use CheckboxSelectMultiple widget for categories field
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', instance=recipe)

        if form.is_valid() and formset.is_valid():
            # Save the form without committing the changes to the database yet
            recipe = form.save(commit=False)

            # Check if a new image is uploaded
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']

            recipe.save()  # Save the recipe instance with the updated image

            recipe.categories.set(form.cleaned_data['categories'])  # Set the categories from the form

            formset.save()  # Save the formset

            return redirect('recipe_detail', recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        form.fields['categories'].widget = CheckboxSelectMultiple()  # Use CheckboxSelectMultiple widget for categories field
        formset = RecipeIngredientFormSet(prefix='ingredients', instance=recipe)

    return render(request, 'update_recipe.html', {
        'form': form,
        'formset': formset,
        'categories': categories,
        'recipe': recipe,
    })



def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipe_list')

def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    context = {'recipe': recipe}
    return render(request, 'recipe_detail.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def recipe_search(request):
    search_input = request.GET.get('keyword', '')
    category_filter = request.GET.getlist('category_filter')

    # Filter recipes by name and description
    recipes = Recipe.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))
    if category_filter:
        recipes = recipes.filter(categories__in=category_filter)

    categories = Category.objects.all()

    return render(request, 'search_results.html', {'recipes': recipes, 'categories': categories})
