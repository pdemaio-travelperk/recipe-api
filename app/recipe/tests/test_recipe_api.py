from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(name: str = "Pizza",
                  description: str = "Sour dough") -> Recipe:
    return Recipe(name=name, description=description)


class RecipeTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_recipes(self):
        sample_recipe()
        sample_recipe(name="Calzone")

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
