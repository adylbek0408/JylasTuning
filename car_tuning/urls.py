from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarBrandViewSet, CarModelViewSet,
    SpoilerViewSet, DiscsViewSet, RestylingViewSet,
    BumperViewSet, RearBumperViewSet, SideSkirtViewSet,
    TintingViewSet, ColorViewSet, UserCarCustomizationViewSet
)

router = DefaultRouter()
router.register(r'brands', CarBrandViewSet)
router.register(r'models', CarModelViewSet)
router.register(r'spoilers', SpoilerViewSet)
router.register(r'discs', DiscsViewSet)
router.register(r'restylings', RestylingViewSet)
router.register(r'bumpers', BumperViewSet)
router.register(r'rear-bumpers', RearBumperViewSet)
router.register(r'side-skirts', SideSkirtViewSet)
router.register(r'tintings', TintingViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'customizations', UserCarCustomizationViewSet, basename='customization')

urlpatterns = [
    path('api/', include(router.urls)),
]
