from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)


def _create_ingredients(recipe: Recipe, ingredients=[]):
    for ingredient in ingredients:
        Ingredient.objects.create(recipe=recipe, name=ingredient['name'])


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializers(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        _create_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        super().update(instance, validated_data)
        if ingredients:
            instance.ingredients.all().delete()
            _create_ingredients(instance, ingredients)

        return instance
