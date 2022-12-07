from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path("", views.recipe_list_view, name='list'),
    path("create/", views.recipe_create_view, name='create'),
    path("hx/<int:id>/", views.recipe_detail_hx_view, name="hx-detail"),

    path("<int:id>/edit/", views.recipe_update_view, name="update"),
    path("<int:id>/", views.recipe_detail_view, name="detail"),
]
