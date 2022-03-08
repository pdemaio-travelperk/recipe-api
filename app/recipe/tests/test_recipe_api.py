import json
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


def sample_ingredient(recipe: Recipe, name: str = "Cucumber") -> Ingredient:
    return Ingredient.objects.create(name=name, recipe=recipe)


def url_for_recipe(recipe_id: str):
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_retrieve_specific_recipe(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(sample_recipe(name="Calzone"))

        res = self.client.get(url_for_recipe(recipe.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeSerializer(recipe).data, res.data)

    def test_retrieve_recipes_by_name_substring(self):
        recipe1 = sample_recipe()
        sample_ingredient(recipe1)
        recipe2 = sample_recipe(name='Calçotada')
        sample_ingredient(recipe2)
        recipe3 = sample_recipe(name='Durum kebab')
        sample_ingredient(recipe3)

        res = self.client.get(RECIPE_URL, {'name': 'Durum'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        serializer = RecipeSerializer(recipe3)
        self.assertIn(serializer.data, res.data)

    def test_create_recipe(self):
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {
                    'name': 'dough'
                },
                {
                    'name': 'cheese'
                },
                {
                    'name': 'tomato'
                }
            ]
        }
        res = self.client.post(RECIPE_URL,
                               json.dumps(payload),
                               content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 1)
        self.assertIsNotNone(res.data['id'])
        self.assertEqual(payload['name'], res.data['name'])
        self.assertEqual(payload['description'],
                         res.data['description'])
        self.assertEqual(len(res.data['ingredients']),
                         len(payload['ingredients']))
        for ingredient in payload['ingredients']:
            self.assertIn(ingredient, res.data['ingredients'])
