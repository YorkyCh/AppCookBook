from django import forms
from .models import Recipe, IngredientAmount, RecipeIngredient, MeasurementUnit
from django_select2 import forms as s2forms
from .models import Ingredient, Category


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'preparation_time', 'image', 'spiciness', 'steps', 'categories')

class IngredientAmountForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=MeasurementUnit.objects.all(), widget=forms.Select(attrs={'class': 'unit-select'}))

    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount', 'unit')

class RecipeIngredientForm(forms.ModelForm):
    ingredient = s2forms.ModelSelect2Widget(
        queryset=Ingredient.objects.all(),
        search_fields=['name__icontains'],
        attrs={'style': 'width: 100%'}
    )
    unit = forms.ModelChoiceField(queryset=MeasurementUnit.objects.all(), widget=s2forms.Select2Widget)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount', 'unit')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            return 1
        return amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].widget.attrs.update({'class': 'ingredient-select'})