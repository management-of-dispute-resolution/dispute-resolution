from rest_framework import mixins, viewsets


class CreteListModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Mixin viewset for GET and POST request."""

    pass
