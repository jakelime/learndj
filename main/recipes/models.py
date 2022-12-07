from django.db import models
from django.urls import reverse
from django.conf import settings
import time

import pint
from . import validators, utils


# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    total_sum = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail", kwargs={"id": self.id})

    def get_ingredients_children(self):
        return self.recipeingredient_set.all()

    def save(self, *args, **kwargs):
        prices = []
        for ingredient in self.get_ingredients_children():
            price = ingredient.quantity_as_float
            if isinstance(price, float):
                prices.append(price)
        total_sum = sum(prices)
        print(f"{total_sum=}")
        if total_sum != self.total_sum:
            self.total_sum = total_sum
            super(Recipe, self).save(*args, **kwargs)
            print(f"Total sum changed: {total_sum = }")
        super().save(*args, **kwargs)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)  # 1 1/4
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validators.validate_unit_of_measure], blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement.to_base_units()

    def as_mks(self):
        # measurement = self.convert_to_system(system='mks')
        time.sleep(0.02)
        # return measurement
        return self.quantity_as_float


    def as_imperial(self):
        # measurement = self.convert_to_system(system='imperial')
        # return measurement
        return self.quantity_as_float


    def save(self, *args, **kwargs):
        qty_as_float, qty_as_float_success = utils.number_str_to_float(self.quantity)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)