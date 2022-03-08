from rest_framework import viewsets

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)

        return queryset.order_by('-id')
