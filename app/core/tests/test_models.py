from unittest import TestCase

from core import models


class ModelTest(TestCase):

    def test_recipe(self):
        recipe = models.Recipe(
            name='Pizza',
            description='Best pizza in the hood',
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient(self):
        ingredient = models.Ingredient(
            name='Tomato',
            recipe=models.Recipe(
                name='Pizza',
                description='Best pizza'
            )
        )

        self.assertEqual(str(ingredient), ingredient.name)
