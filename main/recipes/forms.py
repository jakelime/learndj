from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    error_css_class = "error-field"
    required_css_class = "required-field"
    name = forms.CharField(
        label="Recipe Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Recipe name"}
        ), help_text="HelpText: The name of the recipe"
    )  # input field
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    # descriptions = forms.CharField(
    #     widget=forms.Textarea(attrs={"rows": 3})
    # )  # we can even make new variable that did not exist in the model

    class Meta:
        model = Recipe
        fields = ["name", "description", "directions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            new_data = {
                "placeholder": f"Recipe {str(field)}",
                "class": "form-control",
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["name", "quantity", "unit"]
