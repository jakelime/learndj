from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm


# Create your views here.
@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "objects": qs
    }
    return render(request, "recipes/list.html", context)

@login_required
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id)
    context = {
        "object": obj
    }
    return render(request, "recipes/detail.html", context)



@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    form_2 = RecipeIngredientForm(request.POST or None)
    context = {
        "form": form,
        "form_2": form_2,
        "object": obj,
    }
    if all([form.is_valid(), form_2.is_valid()]):
        form.save(commit=False)
        form_2.save(commit=False)
        print(f"{form.cleaned_data}")
        print(f"{form_2.cleaned_data}")
        # form.save()
        context['message'] = 'Data saved.'
    return render(request, "recipes/create-update.html", context)