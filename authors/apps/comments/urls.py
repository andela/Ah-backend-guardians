from django.urls import path
from .views import (CreateCommentAPiView, CommentApiView,
                    CommentThreadApiView, LikeCommentApiView,
                    GetCommentApiView, CommentHistoryListView)


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
    path('<slug>/comments/<int:id>/likes/',
         LikeCommentApiView.as_view(),
         name='like_comment'),
    path('<slug>/comments/<int:id>/likes/<pk>/',
         GetCommentApiView.as_view(),
         name='retrieve_comment'),
    path(
        '<slug>/comments/<int:id>/history/',
        CommentHistoryListView.as_view(),
        name='comment_history')
]
