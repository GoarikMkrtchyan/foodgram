from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import IngredientViewset, RecipeViewSet, TagViewset, UserViewset

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewset, basename='users')
router_v1.register('tags', TagViewset, basename='tags')
router_v1.register('ingredients', IngredientViewset, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
