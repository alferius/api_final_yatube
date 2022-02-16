from rest_framework.viewsets import GenericViewSet, mixins


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass
