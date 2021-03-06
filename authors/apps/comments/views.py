from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from . import serializers
from .utils import Utils
from .models import Comment, LikeComment, EditHistory
from .renderers import LikeComementsJSONRenderer, CommentJSONRenderer
from authors.apps.articles.models import Article
from rest_framework.generics import get_object_or_404
from .serializers import CommentHistorySerializer


class CreateCommentAPiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CommentSerializer

    queryset = Comment.objects.all()
    util = Utils()

    def post(self, request, *args, **kwargs):
        '''This method creates a comment on an article'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = request.data
        comment.update({ 'article': article.id})
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({"message": "Comment Successfully added"},
                        status=status.HTTP_201_CREATED)

    def get(self, *args, **kwargs):
        '''This method gets all comments for an article'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comments = self.queryset.filter(article_id=article.id)
        serializer = self.serializer_class(comments, many=True)
        return Response({"comments": serializer.data,
                         "commentsCount": comments.count()})


class CommentApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CommentSerializer
    util = Utils()

    def retrieve(self, request, id, *args, **kwargs):
        '''This method gets a single comment by id'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)
        serializer = self.serializer_class(comment)
        return Response({"comment": serializer.data})

    def update(self, request, id, *args, **kwargs):
        '''This method updates a comment'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)

        if request.user.pk == comment.author.id:
            Comment.objects.all().filter(pk=id).update(**request.data)
            EditHistory.objects.create(
                comment=comment, body=comment.body, user=request.user)
            msg = "Comment successfully updated"
            return Response({
                "message": msg
            }, status=status.HTTP_200_OK)
        else:
            msg = {"error": "Unauthorized to update this comment"}
            return Response({
                "message": msg
            }, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, id, *args, **kwargs):
        '''This method deletes a comment'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)

        if request.user.pk == comment.author.id:
            self.perform_destroy(comment)
            msg = "Comment successfully deleted"
            return Response({
                "message": msg
            }, status=status.HTTP_200_OK)
        else:
            msg = {"error": "Unauthorized to delete this comment"}
            return Response({
                "message": msg
            }, status=status.HTTP_401_UNAUTHORIZED)


class CommentThreadApiView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CommentSerializer
    util = Utils()

    def post(self, request, id, *args, **kwargs):
        '''This method comments on a comment creating a thread'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        parent = self.util.check_comment(id)
        comment = request.data
        comment.update({'article': article.id,
                        'parent': id})
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({"message": "Comment Thread Successfully added"},
                        status=status.HTTP_201_CREATED)

    def get(self, request, id, *args, **kwargs):
        '''This method gets an entire thread of comments'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        parent = self.util.check_comment(id)
        thread = self.queryset.filter(article_id=article.id, parent=id)
        serializer = self.serializer_class(thread, many=True)
        return Response({"comments": serializer.data,
                         "thread count": thread.count()})


class LikeCommentApiView(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.LikeCommentSerializer
    renderer_classes = (LikeComementsJSONRenderer, )

    def get_queryset(self):
        return LikeComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Comment.objects.all(), id=id)

    def retrieve(self, request, *args, **kwargs):
        likes = self.get_queryset()
        serializer = self.serializer_class(data=likes, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        data = {
            'comment': comment.id,
            'user': request.user.pk
        }

        like = self.get_queryset().filter(comment=comment.id,
                                          user=request.user.pk)
        if like:
            like.delete()
            return Response({"message": "You have unliked this comment"},
                            status.HTTP_200_OK)
        serializer = self.serializer_class(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "You have liked this comment"},
                        status.HTTP_201_CREATED)


class GetCommentApiView(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.LikeCommentSerializer
    queryset = LikeComment.objects.all()


class CommentHistoryListView(generics.ListAPIView):
    """
    Class For Fetching Comment Edit History
    """
    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentJSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user
        comment = self.kwargs.get('id')
        queryset = EditHistory.objects.filter(user=user, comment=comment)

        serializer = CommentHistorySerializer(
            queryset, many=True)

        if not serializer.data:
            return Response({
                "message": "No Edit History For To This Comment"
            },
                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)
