from rest_framework import viewsets

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')
