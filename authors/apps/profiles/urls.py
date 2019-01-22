from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (RetrieveProfileView, UpdateProfileView,
                    FollowProfileView, RetrieveFollowersView,
                    RetrieveFollowingView, ListProfileView)
from django.urls import path

urlpatterns = {
    path('profiles/', ListProfileView.as_view(), name="show_profile"),
    path('profiles/<username>/', RetrieveProfileView.as_view(),
         name="profile_details"),
    path('profiles/<username>/edit/',
         UpdateProfileView.as_view(), name="update_profile"),
    path('profile/follow/', FollowProfileView.as_view(), name="follow_user"),
    path('profile/followers/', RetrieveFollowersView.as_view(),
         name="followers"),
    path('profile/following/', RetrieveFollowingView.as_view(),
         name="following"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
