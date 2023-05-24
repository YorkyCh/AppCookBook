from django import forms
from .models import Recipe, IngredientAmount, RecipeIngredient, MeasurementUnit
from django_select2 import forms as s2forms
from .models import Ingredient, Category
from django.forms.widgets import ClearableFileInput
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(image):
    file_size = image.size
    width, height = get_image_dimensions(image)
    max_size = 1024 * 1024  # 1MB
    max_width = 800  # pixels
    max_height = 800  # pixels

    if width > max_width or height > max_height:
        raise ValidationError("Max size of an image is %s x %s" % (max_width, max_height))
    if file_size > max_size:
        raise ValidationError("Max file size is: %sKB" % str(max_size // 1024))

class CustomClearableFileInput(ClearableFileInput):
    def get_template_substitution_values(self, value):
        return {
            'initial': self.initial_text,
            'clear_template': '',
            'input_text': '',
            'is_initial': bool(value),
            'value': value,
            'template_name': self.template_name,
        }


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        error_messages={'required': 'Please select at least one category.'}
    )
    image = forms.ImageField(widget=CustomClearableFileInput, validators=[validate_image], error_messages={'required': 'Please upload an image.'})
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'wide-textarea'}), error_messages={'required': 'Please provide a description.'})
    steps = forms.CharField(widget=forms.Textarea, required=True, error_messages={'required': 'Please provide the steps.'})
    portion_size = forms.IntegerField(min_value=1, initial=1, required=True, error_messages={'required': 'Please provide the portion size.'})
    
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'preparation_time', 'image', 'spiciness', 'steps', 'categories', 'portion_size')

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')

        if not categories:
            self.add_error('categories', self.fields['categories'].error_messages['required'])

        return cleaned_data

class IngredientAmountForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=MeasurementUnit.objects.all(), widget=forms.Select(attrs={'class': 'unit-select'}), required=False)  # Made unit optional

    class Meta:
        model = IngredientAmount
        exclude = ('id',)  # Excluded 'id' field

class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), widget=forms.Select(attrs={'class': 'ingredient-select'}))
    unit = forms.ModelChoiceField(queryset=MeasurementUnit.objects.all(), widget=forms.Select(attrs={'class': 'ingredient-select'}))

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'amount', 'unit')  # Include the 'id' field
        widgets = {
            'unit': forms.Select(attrs={'class': 'ingredient-select'}),
        }
        labels = {
            'ingredient': 'Ingredient',
            'amount': 'Amount',
            'unit': 'Unit',
        }
        error_messages = {
            'ingredient': {
                'required': 'Please select an ingredient.',
            },
            'amount': {
                'required': 'Please enter the amount.',
            },
            'unit': {
                'required': 'Please select a unit.',
            },
        }
