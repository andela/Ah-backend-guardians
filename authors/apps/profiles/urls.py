from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RetrieveProfileView, UpdateProfileView
from django.urls import path

urlpatterns = {
    path('profiles/<username>/',
         RetrieveProfileView.as_view(), name="profile_details"),
    path('profiles/<username>/edit/',
         UpdateProfileView.as_view(), name="update_profile"),

}

urlpatterns = format_suffix_patterns(urlpatterns)
