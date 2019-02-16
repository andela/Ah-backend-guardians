from .views import ListNotificationsView
from django.urls import include, path


urlpatterns = [
    path('all/', ListNotificationsView.as_view(),
         name='notifications')
]
