# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, inlineformset_factory
from .models import Recipe, Ingredient, Category, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm
from django.db.models import Q 

def add_recipe(request):
    RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, fields=('ingredient', 'amount'), extra=1)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients')
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            categories = request.POST.getlist('categories')
            recipe.categories.set(categories)

            for ingredient_form in formset:
                if ingredient_form.cleaned_data:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            return redirect('recipe_detail', recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(prefix='ingredients')
        categories = Category.objects.all()

    return render(request, 'add_recipe.html', {'form': form, 'formset': formset, 'categories': categories})

def update_recipe(request, pk):
    print("Request URL:", request.build_absolute_uri())
    print("POST Data:", request.POST)
    recipe = get_object_or_404(Recipe, pk=pk)
    RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, fields=('ingredient', 'amount'), extra=0)
    
    categories = Category.objects.all()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', instance=recipe)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            recipe.recipeingredient_set.all().delete()
            categories_selected = request.POST.getlist('categories')
            recipe.categories.set(categories_selected)

            for ingredient_form in formset:
                if ingredient_form.cleaned_data:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            return redirect('recipe_detail', pk=recipe.pk)
        
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(prefix='ingredients', instance=recipe)

    return render(request, 'update_recipe.html', {'form': form, 'formset': formset, 'categories': categories, 'recipe': recipe})



def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipes_list')

def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    context = {'recipe': recipe}
    return render(request, 'recipe_detail.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {'ingredients': ingredients})

def recipe_search(request):
    search_input = request.GET.get('search_input', '')
    category_filter = request.GET.get('category_filter', '')
    if category_filter:
        category = Category.objects.get(pk=category_filter)
        recipes = Recipe.objects.filter(categories=category, name__icontains=search_input)
    else:
        recipes = Recipe.objects.filter(name__icontains=search_input)

    return render(request, 'search_results.html', {'recipes': recipes})

def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def recipe_search(request):
    search_input = request.GET.get('search_input', '')
    category_filter = request.GET.get('category_filter', '')

    if category_filter:
        category = Category.objects.get(pk=category_filter)
        recipes = Recipe.objects.filter(categories=category, name__icontains=search_input)
    else:
        recipes = Recipe.objects.filter(name__icontains=search_input)

    return render(request, 'search_results.html', {'recipes': recipes})