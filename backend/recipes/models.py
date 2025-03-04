import random
import string

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from recipes.constants import (LIMIT_INGREDIENT_NAME, LIMIT_RECIPE_NAME,
                               LIMIT_SHORT_LINK, LIMIT_TAG_NAME, MIN_LIMIT)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=LIMIT_TAG_NAME,
        unique=True,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=LIMIT_TAG_NAME,
        unique=True,
        verbose_name='Cлаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=LIMIT_INGREDIENT_NAME,
        unique=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=LIMIT_INGREDIENT_NAME,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=LIMIT_RECIPE_NAME,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(limit_value=MIN_LIMIT)
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Теги рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты рецепта'
    )

    short_link = models.CharField(
        max_length=LIMIT_SHORT_LINK,
        blank=True,
        unique=True,
        null=True,
        verbose_name='Короткая ссылка рецепта',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def generate_short_link(self):
        while (short_link := ''.join(random.choices(
            string.ascii_letters + string.digits, k=LIMIT_SHORT_LINK))
        ) is not Recipe.objects.filter(short_link=short_link).exists():
            return short_link

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = self.generate_short_link()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk and not self.ingredients.exists():
            raise ValidationError("Рецепт должен содержать 1 ингредиент.")


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tag',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='recipe_tag_unique'
            )
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество ингредиента',
        validators=[
            MinValueValidator(limit_value=MIN_LIMIT)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe_ingredient_unique'
            )
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='favorite_unique'
            )
        ]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name = 'Корзины покупок'

        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='shopping_cart_unique'
            )
        ]
