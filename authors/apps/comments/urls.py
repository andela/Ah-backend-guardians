from django.urls import path
from .views import CreateCommentAPiView, CommentApiView, CommentThreadApiView


urlpatterns = [
    path('<slug>/comments/',
         CreateCommentAPiView.as_view(),
         name='comment'),
    path('<slug>/comments/<int:id>/',
         CommentApiView.as_view(),
         name='specific_comment'),
    path('<slug>/comments/<int:id>/thread/',
         CommentThreadApiView.as_view(),
         name='comment_thread'),
]
