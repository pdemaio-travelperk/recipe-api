from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(name: str = "Pizza",
                  description: str = "Sour dough") -> Recipe:
    return Recipe.objects.create(name=name, description=description)


def sample_ingredient(recipe: Recipe, name: str = "Sample ingredient"):
    Ingredient.objects.create(name=name, recipe=recipe)


class RecipeTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_recipes(self):
        recipe1 = sample_recipe()
        recipe2 = sample_recipe(name="Calzone")
        sample_ingredient(recipe1)
        sample_ingredient(recipe2)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
