from django.urls import path
from .views import MapView

app_name = "map"

urlpatterns = [
    # This URL is being parsed, city must be an existing city name in database,
    # and observatory name the one indicated in the city object.
    path('g', MapView.as_view(), name="map"),
]
