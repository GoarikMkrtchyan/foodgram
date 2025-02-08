from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.constants import MIN_AMOUNT
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Follow

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if (request
                and request.user.is_authenticated
                and obj.following.filter(user=request.user).exists()):
            return True
        return False

    def validate(self, data):
        if not data.get('avatar'):
            raise serializers.ValidationError(
                {'avatar': 'Поле не может быть пустым!'})
        return data


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError()
        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name',
            'measurement_unit', 'amount',
        )


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    def validate_amount(self, amount):
        if amount < MIN_AMOUNT:
            raise serializers.ValidationError(
                'Добавьте количество ингредиента'
            )
        return amount


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True, read_only=True
    )
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='ingredient'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return obj.favorite.filter(
            user=user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(
            user=user
        ).exists()


class EasyRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )
        read_only_fields = '__all__',


class CreateRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientInRecipeSerializer(
        many=True,
        required=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate_image(self, image_data):
        if not image_data:
            raise serializers.ValidationError(
                'Поле Картинка не должно быть пустым'
            )
        return image_data

    def validate(self, data):
        if 'ingredients' not in data:
            raise serializers.ValidationError()
        ingredients = data.get('ingredients')
        if 'tags' not in data:
            raise serializers.ValidationError()
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError(
                'Список ингредиентов не может быть пустым!'
            )
        if not tags:
            raise serializers.ValidationError(
                'Список ингредиентов не может быть пустым!'
            )
        unique_ingredients = {
            ingredient.get('id') for ingredient in ingredients
        }
        if len(unique_ingredients) != len(ingredients):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться'
            )
        tag_set = set(tags)
        if len(tag_set) != len(tags):
            raise serializers.ValidationError(
                'Теги не должны повторяться'
            )
        return data

    def set_tags_ingredients(self, recipe, tags, ingredients):
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            ) for ingredient in ingredients]
        )
        recipe.tags.set(tags, clear=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.set_tags_ingredients(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.ingredients.clear()
        self.set_tags_ingredients(instance, tags, ingredients)
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data


class SubscriptionShowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request:
            recipes_limit = request.GET.get('recipes_limit')
            if recipes_limit is not None:
                recipes = obj.recipes.all()[:int(recipes_limit)]
            else:
                recipes = obj.recipes.all()
            serializer = EasyRecipeSerializer(
                recipes,
                many=True
            )
            return serializer.data
        return []

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = (
            'user', 'following',
        )

    def validate(self, data):
        user = data.get('user')
        following = data.get('following')
        if user == following:
            raise serializers.ValidationError(
                'Нельзя отписаться или подписаться на самого себя'
            )
        if Follow.objects.filter(
            user=user,
            following=following
        ).exists():
            raise serializers.ValidationError(
                'Подписка уже оформлена'
            )
        return data

    def to_representation(self, instance):
        return SubscriptionShowSerializer(
            instance.following,
            context={
                'request': self.context.get('request')
            }
        ).data
