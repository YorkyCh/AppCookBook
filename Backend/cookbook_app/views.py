from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, inlineformset_factory
from .models import Recipe, Ingredient, Category, IngredientAmount, MeasurementUnit, RecipeIngredient
from .forms import RecipeForm, IngredientAmountForm, RecipeIngredientForm
from django.db.models import Q 
from django.forms.widgets import CheckboxSelectMultiple
from django.db.models import F


def add_recipe(request):
    RecipeIngredientFormSet = inlineformset_factory(
        Recipe,
        RecipeIngredient,
        form=RecipeIngredientForm,
        fields=('ingredient', 'amount', 'unit'),
        extra=1
    )

    categories = Category.objects.all()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', queryset=RecipeIngredient.objects.none())

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.portion_size = form.cleaned_data['portion_size']
            recipe.base_portion_size = form.cleaned_data['portion_size']  # Set the base portion size when creating the recipe
            recipe.save()

            recipe.categories.set(form.cleaned_data['categories'])

            for ingredient_form in formset:
                if ingredient_form.cleaned_data:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            return redirect('recipe_detail', pk=recipe.pk)
        else:
            print(form.errors)
            print(formset.errors)

        
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(
            prefix='ingredients',
            queryset=RecipeIngredient.objects.none(),
            initial=[{'ingredient': ingredient} for ingredient in Ingredient.objects.all()]  # Add initial data for ingredient field
        )

    return render(request, 'add_recipe.html', {
        'form': form,
        'formset': formset,
        'categories': categories,
    })

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
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', instance=recipe)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)

            # Update the base_portion_size if the portion_size has changed in the form
            if 'portion_size' in form.changed_data:
                recipe.base_portion_size = form.cleaned_data['portion_size']

            recipe.save()

            if 'image' in request.FILES:
                recipe.image = request.FILES['image']

            recipe.save()

            # Clear existing categories and set the selected categories from the form
            recipe.categories.clear()
            categories_ids = request.POST.getlist('categories')
            categories = Category.objects.filter(id__in=categories_ids)
            recipe.categories.set(categories)

            formset_instances = formset.save(commit=False)
            for formset_instance in formset_instances:
                formset_instance.recipe = recipe  # Set the recipe instance for each formset instance
                formset_instance.save()

            formset.save_m2m()

            # Reconstruct the form with updated category data
            form = RecipeForm(instance=recipe)
            form.fields['categories'].widget = CheckboxSelectMultiple()
            form.fields['categories'].queryset = Category.objects.all()
            form.fields['categories'].initial = recipe.categories.all()
            form.fields['portion_size'].initial = recipe.portion_size  # Set the initial portion size
            formset = RecipeIngredientFormSet(prefix='ingredients', instance=recipe)

            return redirect('recipe_detail', recipe.pk)

        else:
            print(form.errors)
            print(formset.errors)

    else:
        form = RecipeForm(instance=recipe)
        form.fields['categories'].widget = CheckboxSelectMultiple()
        form.fields['categories'].queryset = Category.objects.all()
        form.fields['categories'].initial = recipe.categories.all()
        form.fields['portion_size'].initial = recipe.portion_size  # Set the initial portion size
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
    recipe = get_object_or_404(Recipe, pk=pk)
    initial_portion_size = recipe.base_portion_size

    if request.method == 'POST':
        new_portion_size = int(request.POST.get('portion_size', 1))
        recipe.portion_size = new_portion_size
        recipe.save()

    ingredient_amounts = []
    for ingredient_amount in recipe.recipeingredient_set.all():
        adjusted_amount = round((float(ingredient_amount.amount) * int(recipe.portion_size)) / int(recipe.base_portion_size), 2)  # Use base_portion_size here
        ingredient_amounts.append({
            'ingredient': ingredient_amount.ingredient,
            'adjusted_amount': adjusted_amount,
            'unit': ingredient_amount.unit
        })
    steps = recipe.steps.split("\n") if recipe.steps else []

    context = {
        'recipe': recipe,
        'ingredient_amounts': ingredient_amounts,
        'steps': steps,
    }
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