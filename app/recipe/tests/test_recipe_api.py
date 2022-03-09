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

    def test_retrieve_non_existent_recipe(self):
        res = self.client.get(url_for_recipe(123))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

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

    def test_create_invalid_recipe_without_ingredients(self):
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
        }
        res = self.client.post(RECIPE_URL,
                               json.dumps(payload),
                               content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_recipe_without_name(self):
        payload = {
            'name': '',
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
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_recipe_without_description(self):
        payload = {
            'name': 'Pizza',
            'description': '',
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
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_recipe_without_ingredient_name(self):
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {
                    'name': ''
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
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipe_edit(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [{'name': 'casa-tarradellas'}]
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.id, res.data['id'])
        self.assertEqual(payload['name'], res.data['name'])
        self.assertEqual(payload['description'],
                         res.data['description'])
        self.assertEqual(payload['ingredients'], res.data['ingredients'])

    def test_recipe_edit_remove_ingredients(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.id, res.data['id'])
        self.assertEqual(payload['name'], res.data['name'])
        self.assertEqual(payload['description'],
                         res.data['description'])
        self.assertEqual(recipe.ingredients.count(),
                         len(res.data['ingredients']))

    def test_recipe_edit_remove_ingredients_with_empty_list(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': []
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.id, res.data['id'])
        self.assertEqual(payload['name'], res.data['name'])
        self.assertEqual(payload['description'],
                         res.data['description'])
        self.assertEqual(recipe.ingredients.count(),
                         len(res.data['ingredients']))

    def test_recipe_invalid_edit_remove_name(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': '',
            'description': 'Put it in the oven',
            'ingredients': [{'name': 'casa-tarradellas'}]
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipe_invalid_edit_remove_description(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': 'Pizza',
            'description': '',
            'ingredients': [{'name': 'casa-tarradellas'}]
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipe_invalid_edit_remove_ingredient_name(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'tomato')

        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [{'name': ''}]
        }

        res = self.client.patch(url_for_recipe(recipe.id),
                                json.dumps(payload),
                                content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_recipe(self):
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe, 'lettuce')

        recipes_before = Recipe.objects.count()
        ingredients_before = Ingredient.objects.count()
        ingredients_now = ingredients_before - recipe.ingredients.count()
        res = self.client.delete(url_for_recipe(recipe.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), ingredients_now)
        self.assertEqual(Recipe.objects.all().count(), recipes_before-1)
