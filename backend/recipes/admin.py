from django.contrib import admin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, RecipeTagInLine,)
    list_display = (
        'name', 'author', 'favorite_count',
        'ingredients_in_recipe', 'tags_in_recipe',
    )
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tags__name',)

    @admin.display(description='Добавили в избранное')
    def favorite_count(self, obj):
        return obj.favorite.count()

    @admin.display(description='Теги рецепта')
    def tags_in_recipe(self, obj):
        tags = obj.recipe_tag.values('tag__name').order_by('tag__name')
        return ', '.join([tag['tag__name'] for tag in tags])

    @admin.display(description='Ингредиенты рецепта')
    def ingredients_in_recipe(self, obj):
        ingredients = (
            RecipeIngredient.objects.filter(recipe=obj)
            .values(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
            )
            .order_by(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
        )
        return ', '.join(
            [
                (
                    f"{ingredient['ingredient__name']} - "
                    f"{ingredient['amount']} "
                    f"{ingredient['ingredient__measurement_unit']}"
                )
                for ingredient in ingredients
            ]
        )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_filter = ('name',)
    search_fields = ('name', 'slug',)


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ("recipe", "tag",)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient, IngredientAdmin)
