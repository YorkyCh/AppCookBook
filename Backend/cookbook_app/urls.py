from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('recipes/', views.recipe_list, name='recipes_list'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('recipes/<int:pk>/update/', views.update_recipe, name='update_recipe'),
    path('', views.index, name='index'),
    path('recipe_search/', views.recipe_search, name='recipe_search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)