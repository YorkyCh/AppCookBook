from django import forms
from .models import Recipe, IngredientAmount, RecipeIngredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'preparation_time', 'cook_time', 'image', 'spiciness', 'steps')

class IngredientAmountForm(forms.ModelForm):
    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount', 'unit')

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            return 1
        return amount