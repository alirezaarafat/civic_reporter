from rest_framework.routers import DefaultRouter

from .views import AreaViewSet, CategoryViewSet

router = DefaultRouter()
router.register("areas", AreaViewSet, basename="area")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = router.urls
