from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)


class IngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]

        if not valid_forms:
            for form in self.forms:
                form.add_error(
                    None, "Рецепт должен содержать хотя бы 1 ингредиент.")

        for form in valid_forms:
            amount = form.cleaned_data.get('amount')
            if amount is not None and amount <= 0:
                form.add_error(
                    'amount', "Количество ингредиента должно быть больше 0.")


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    formset = IngredientFormSet


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    extra = 1


class RecipeForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients', [])

        if not ingredients:
            self.add_error(
                'ingredients', "Рецепт должен содержать 1 ингредиент")

        for ingredient in ingredients:
            if ingredient.amount <= 0:
                self.add_error(
                    'ingredients', "Количество ингредиента должно быть > 0")

        return cleaned_data


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
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

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(
                request, f"Ошибка: {e.messages[0]}", level=messages.ERROR)


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
