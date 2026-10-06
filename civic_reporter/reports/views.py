from rest_framework import permissions, viewsets

from .models import Area, Category
from .serializers import AreaSerializer, CategorySerializer


class AreaViewSet(viewsets.ModelViewSet):
    """
    /api/reports/areas/        GET, POST
    /api/reports/areas/{id}/   GET, PUT, PATCH, DELETE
    Read is open to any logged-in user; write intended for authorities/admins
    (tighten permission_classes once AuthorityProfile-based permissions are added).
    """

    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
