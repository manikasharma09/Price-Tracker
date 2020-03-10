from django.contrib import admin
from django.urls import path
from tracker.views import tracker_view

urlpatterns = [
    path('admin', admin.site.urls),
    path('', tracker_view, name="tracker"),
]
