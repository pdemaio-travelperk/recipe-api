from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializers(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, name=ingredient['name'])

        return recipe
