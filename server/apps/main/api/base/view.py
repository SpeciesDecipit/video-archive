from typing import Dict, Type

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


class SerializerMappingModelViewSet(ModelViewSet):
    """Class adds serializer mapping logic depends on request method."""

    serializers_mapping: Dict[str, Type[ModelSerializer]] = {}

    def get_serializer_class(self) -> Type[ModelSerializer]:
        """Method returns the class to use for the serializer."""
        return self.serializers_mapping[self.request.method]
